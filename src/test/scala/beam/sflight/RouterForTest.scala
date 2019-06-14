package beam.sflight

import akka.actor.{ActorRef, PoisonPill}
import akka.testkit.{ImplicitSender, TestKitBase}
import beam.router.BeamRouter
import beam.sim.BeamScenario
import beam.sim.common.GeoUtilsImpl
import beam.utils.{NetworkHelperImpl, SimRunnerForTest}
import org.scalatest.{BeforeAndAfterAll, Suite}

import scala.language.postfixOps

trait RouterForTest extends BeforeAndAfterAll with ImplicitSender {
  this: Suite with SimRunnerForTest with TestKitBase =>

  var router: ActorRef = _

  override def beforeAll: Unit = {
    super.beforeAll()
    val beamScenario = injector.getInstance(classOf[BeamScenario])
    router = system.actorOf(
      BeamRouter.props(
        beamScenario,
        beamScenario.transportNetwork,
        beamScenario.network,
        new NetworkHelperImpl(beamScenario.network),
        new GeoUtilsImpl(beamScenario.beamConfig),
        scenario,
        scenario.getTransitVehicles,
        fareCalculator,
        tollCalculator
      )
    )
    services.beamRouter = router // :-(
  }

  override def afterAll(): Unit = {
    router ! PoisonPill
    super.afterAll()
  }

}
