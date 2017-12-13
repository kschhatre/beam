package beam.sim

import java.util.concurrent.TimeUnit

import akka.actor.{ActorRef, ActorSystem, Identify, PoisonPill, Props}
import akka.pattern.ask
import akka.util.Timeout
import beam.agentsim
import beam.agentsim.agents.BeamAgent.Finish
import beam.agentsim.agents._
import beam.agentsim.agents.household.HouseholdActor
import beam.agentsim.agents.household.HouseholdActor.InitializeRideHailAgent
import beam.agentsim.agents.vehicles.BeamVehicleType.{CarVehicle, HumanBodyVehicle}
import beam.agentsim.agents.vehicles.EnergyEconomyAttributes.Powertrain
import beam.agentsim.agents.vehicles._
import beam.agentsim.scheduler.BeamAgentScheduler
import beam.agentsim.scheduler.BeamAgentScheduler.StartSchedule
import beam.router.BeamRouter.InitTransit
import beam.sim.monitoring.ErrorListener
import com.google.inject.Inject
import org.apache.log4j.Logger
import org.matsim.api.core.v01.population.Person
import org.matsim.api.core.v01.{Coord, Id, Scenario}
import org.matsim.core.api.experimental.events.EventsManager
import org.matsim.core.mobsim.framework.Mobsim
import org.matsim.households.Household
import org.matsim.vehicles.{Vehicle, VehicleType}

import scala.collection.JavaConverters
import scala.collection.JavaConverters._
import scala.concurrent.Await

/**
  * AgentSim entrypoint.
  * Should instantiate the [[ActorSystem]], [[BeamServices]] and interact concurrently w/ the QSim.
  *
  * Created by sfeygin on 2/8/17.
  */
class BeamMobsim @Inject()(val beamServices: BeamServices, val scenario: Scenario, val eventsManager: EventsManager, val actorSystem: ActorSystem) extends Mobsim {
  private implicit val timeout = Timeout(50000, TimeUnit.SECONDS)

  private val log = Logger.getLogger(classOf[BeamMobsim])
  private val errorListener = actorSystem.actorOf(ErrorListener.props())
  actorSystem.eventStream.subscribe(errorListener, classOf[BeamAgent.TerminatedPrematurelyEvent])

  var rideHailingAgents: Seq[ActorRef] = Nil

  override def run() = {
    eventsManager.initProcessing()

    beamServices.schedulerRef = actorSystem.actorOf(Props(classOf[BeamAgentScheduler], beamServices.beamConfig, 3600 * 30.0, 300.0), "scheduler")
    beamServices.rideHailingManager = actorSystem.actorOf(RideHailingManager.props("RideHailingManager", Map[Id[VehicleType], BigDecimal](), beamServices.vehicles.toMap, beamServices, Map.empty))

    resetPop()

    Await.result(beamServices.beamRouter ? InitTransit, timeout.duration)
    log.info(s"Transit schedule has been initialized")

    log.info("Running BEAM Mobsim")
    Await.result(beamServices.schedulerRef ? StartSchedule(0), timeout.duration)
    cleanupRideHailingAgents()
    cleanupVehicle()
    cleanupHouseHolder()
    actorSystem.stop(beamServices.schedulerRef)

    eventsManager.finishProcessing()
  }


  private def cleanupRideHailingAgents(): Unit = {
    rideHailingAgents.foreach(_ ! Finish)
    rideHailingAgents = Nil
  }

  private def cleanupVehicle(): Unit = {
    // FIXME XXXX (VR): Probably no longer necessary
    log.info(s"Removing Humanbody vehicles")
    for (personId <- beamServices.persons.keys) {
      val bodyVehicleId = HumanBodyVehicle.createId(personId)
      beamServices.vehicles -= bodyVehicleId
    }
  }

  private def cleanupHouseHolder(): Unit = {
    for ((_, householdAgent) <- beamServices.householdRefs) {
      log.debug(s"Stopping ${householdAgent.path.name} ")
      householdAgent ! PoisonPill
    }
  }

  def resetPop(): Unit = {
    beamServices.persons ++= scala.collection.JavaConverters.mapAsScalaMap(scenario.getPopulation.getPersons)
    beamServices.households ++= scenario.getHouseholds.getHouseholds.asScala.toMap
    log.info(s"Loaded ${beamServices.persons.size} people in ${beamServices.households.size} households with ${beamServices.vehicles.size} vehicles")

    val population = actorSystem.actorOf(Population.props(beamServices, eventsManager), "population")
    Await.result(population ? Identify(0), timeout.duration)

    // Init households before RHA.... RHA vehicles will initially be managed by households
    initHouseholds()

    // Init ridehailing agents
    sampleRideHailAgentsFromPop(
      beamServices.beamConfig.beam.agentsim.agents.rideHailing.numDriversAsFractionOfPopulation)


  }


  private def sampleRideHailAgentsFromPop(fraction: Double): Unit = {
    val numRideHailAgents: Int = math
      .round(math.min(
        beamServices.beamConfig.beam.agentsim.numAgents,
        beamServices.persons.size) * beamServices.beamConfig.beam.agentsim.agents.rideHailing
        .numDriversAsFractionOfPopulation)
      .toInt
    var totalRideShareAgents: Int = 0
    for {
      (hId: Id[Household], hh: Household) <- beamServices.households
      mId: Id[Person] <- JavaConverters.asScalaBuffer(hh.getMemberIds)
    } yield {
      totalRideShareAgents += 1
      if (totalRideShareAgents < numRideHailAgents) {
        beamServices.householdRefs(hId) ! InitializeRideHailAgent(mId)
      }
    }
    log.info(s"Initialized $numRideHailAgents ride hailing agents")
  }


  private def initHouseholds(iterId: Option[String] = None)(implicit ev: Id[Vehicle] => Id[BeamVehicle]): Unit = {
    val householdAttrs = scenario.getHouseholds.getHouseholdAttributes


    beamServices.households.foreach {
      case (householdId, matSimHousehold) =>
        //TODO a good example where projection should accompany the data
        if (householdAttrs.getAttribute(householdId.toString, "homecoordx") == null) {
          log.error(
            s"Cannot find homeCoordX for household $householdId which will be interpreted at 0.0")
        }
        if (householdAttrs.getAttribute(householdId.toString.toLowerCase(),
          "homecoordy") == null) {
          log.error(
            s"Cannot find homeCoordY for household $householdId which will be interpreted at 0.0")
        }
        val homeCoord = new Coord(
          householdAttrs
            .getAttribute(householdId.toString, "homecoordx")
            .asInstanceOf[Double],
          householdAttrs
            .getAttribute(householdId.toString, "homecoordy")
            .asInstanceOf[Double]
        )

        val membersActors = matSimHousehold.getMemberIds.asScala
          .map { personId =>
            (personId, beamServices.personRefs.get(personId))
          }
          .collect {
            case (personId, Some(personAgent)) => (personId, personAgent)
          }
          .toMap


        val houseHoldVehicles: Map[Id[BeamVehicle], BeamVehicle] = JavaConverters
          .collectionAsScalaIterable(matSimHousehold.getVehicleIds)
          .map({ id =>
            val matsimVehicle = JavaConverters.mapAsScalaMap(
              scenario.getVehicles.getVehicles)(
              id)
            val information = Option(matsimVehicle.getType.getEngineInformation)
            val vehicleAttribute = Option(
              scenario.getVehicles.getVehicleAttributes)
            val powerTrain = Powertrain.PowertrainFromMilesPerGallon(
              information
                .map(_.getGasConsumption)
                .getOrElse(Powertrain.AverageMilesPerGallon))
            agentsim.vehicleId2BeamVehicleId(id) -> new BeamVehicle(None,
              powerTrain,
              matsimVehicle,
              vehicleAttribute,
              CarVehicle)
          }).toMap

        houseHoldVehicles.foreach(x => beamServices.vehicles.update(x._1, x._2))

        val props = HouseholdActor.props(beamServices, eventsManager, scenario.getPopulation, householdId, matSimHousehold, houseHoldVehicles, membersActors, homeCoord)

        val householdActor = actorSystem.actorOf(
          props,
          HouseholdActor.buildActorName(householdId, iterId))

        houseHoldVehicles.values.foreach { veh => veh.manager = Some(householdActor) }


        beamServices.householdRefs.put(householdId, householdActor)
    }
  }

}



