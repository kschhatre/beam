package beam.agentsim.agents.ridehail

import akka.actor.{Actor, Props}
import beam.agentsim.agents.ridehail.RideHailIterationHistoryActor._
import beam.sim.BeamServices
import beam.utils.DebugLib
import com.conveyal.r5.transit.TransportNetwork
import org.matsim.core.api.experimental.events.EventsManager

class RideHailIterationHistoryActor(
  eventsManager: EventsManager,
  beamServices: BeamServices,
  transportNetwork: TransportNetwork
) extends Actor {

  //val rideHailIterationHistory=scala.collection.mutable.ListBuffer( Map[String, ArrayBuffer[Option[RideHailStatsEntry]]])
  // TODO: put in RideHailStats class!
  // create methods in that class, which I need for my programming

  // TODO: how get a reference of RideHailIterationHistoryActor to the rideHailManager?

  val rideHailIterationStatsHistory =
    scala.collection.mutable.ArrayBuffer[TNCIterationStats]()

  def oszilationAdjustedTNCIterationStats(): Option[TNCIterationStats] = {
    if (rideHailIterationStatsHistory.size >= 2) {
      val lastElement = rideHailIterationStatsHistory.last
      val secondLastElement = rideHailIterationStatsHistory(rideHailIterationStatsHistory.size - 2)
      Some(TNCIterationStats.merge(lastElement, secondLastElement))
    } else {
      rideHailIterationStatsHistory.lastOption
    }
  }

  def receive = {

    case GetCurrentIterationRideHailStats => //tNCIterationsStatsCollector.rideHailStats // received message from RideHailManager
      val stats = oszilationAdjustedTNCIterationStats()
      //  stats.foreach(_.printMap())
      sender() ! stats
    //sender() ! UpdateHistoricWaitingTimes(null)

    case UpdateRideHailStats(stats) =>
      rideHailIterationStatsHistory += stats

      // trimm array buffer as we just need 2 elements
      if (rideHailIterationStatsHistory.size > 2) {
        rideHailIterationStatsHistory.remove(0)
      }

    case _ =>
      DebugLib.emptyFunctionForSettingBreakPoint()
    // TODO: add logger!
  }
}

object RideHailIterationHistoryActor {

  case class UpdateRideHailStats(rideHailStats: TNCIterationStats)

  case class AddTNCHistoryData(
    tncIdleTimes: Set[WaitingEvent],
    passengerWaitingTimes: Set[WaitingEvent]
  )

  case object GetCurrentIterationRideHailStats

  case class UpdateHistoricWaitingTimes(historicWaitingTimes: HistoricWaitingTimes)

  case class HistoricWaitingTimes()

  case class CollectRideHailStats()

  def props(
    eventsManager: EventsManager,
    beamServices: BeamServices,
    transportNetwork: TransportNetwork
  ) =
    Props(new RideHailIterationHistoryActor(eventsManager, beamServices, transportNetwork))
}