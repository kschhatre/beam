package beam.physsim.bprsim

import org.matsim.api.core.v01.Scenario
import org.matsim.api.core.v01.events.Event
import org.matsim.api.core.v01.population.{Activity, Person}
import org.matsim.core.api.experimental.events.EventsManager
import org.matsim.core.mobsim.framework.Mobsim
import org.matsim.core.mobsim.jdeqsim.JDEQSimConfigGroup.PRIORITY_DEPARTUARE_MESSAGE

import scala.annotation.tailrec
import scala.collection.JavaConverters._
import scala.collection.mutable

/**
  *
  * @author Dmitry Openkov
  */
class BPRSimulation(scenario: Scenario, config: BPRSimConfig, eventManager: EventsManager) extends Mobsim {
  private val queue = mutable.PriorityQueue.empty[SimEvent](BPRSimulation.simEventOrdering)
  private val params = BPRSimParams(config, new VolumeCalculator(config.inFlowAggregationTimeWindow))

  override def run(): Unit = {
    val persons = scenario.getPopulation.getPersons.values().asScala
    persons
      .map(person => BPRSimulation.startingEvent(person, _ => true))
      .flatMap(_.iterator)
      .foreach(queue.enqueue(_))

    processQueuedEvents()
  }

  @tailrec
  private def processQueuedEvents(): Unit = {
    if (queue.nonEmpty) {
      val simulationEvent = queue.dequeue()
      simulationEvent.execute(scenario, params) match {
        case (events, simEvent) =>
          events.foreach(eventManager.processEvent)
          for {
            e <- simEvent if e.time < config.simEndTime
          } queue += e
      }
      processQueuedEvents()
    }
  }
}

object BPRSimulation {
  implicit val eventTimeOrdering: Ordering[Event] = (x: Event, y: Event) => {
    java.lang.Double.compare(x.getTime, y.getTime)
  }

  private[bprsim] val simEventOrdering: Ordering[SimEvent] = (x: SimEvent, y: SimEvent) => {
    val c1 = java.lang.Double.compare(y.time, x.time)
    if (c1 != 0) c1 else java.lang.Integer.compare(x.priority, y.priority)
  }

  private[bprsim] def startingEvent(person: Person, accept: Activity => Boolean): Option[StartLegSimEvent] = {
    val plan = person.getSelectedPlan
    if (plan == null || plan.getPlanElements.size() <= 1)
      None
    else {
      // actsLegs(0) is the first activity, actsLegs(1) is the first leg
      val firstAct = plan.getPlanElements.get(0).asInstanceOf[Activity]
      if (accept(firstAct)) {
        // an agent starts the first leg at the end_time of the fist act
        val departureTime = firstAct.getEndTime

        // schedule start leg message
        Some(new StartLegSimEvent(departureTime, PRIORITY_DEPARTUARE_MESSAGE, person, 1))
      } else {
        None
      }
    }
  }
}