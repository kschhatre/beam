package beam.side.speed

import java.nio.file.Path

import scala.util.{Failure, Success, Try}

case class CompareConfig(uberSpeedPath: String = "", osmMapPath: String = "")

trait AppSetup {

  val parser = new scopt.OptionParser[CompareConfig]("speedcompare") {
    head("Uber with BEAM Speed Compare App", "version 1.0")

    opt[String]('u', "uber")
      .required()
      .valueName("<user_path>")
      .action((s, c) => c.copy(uberSpeedPath = s))
      .validate(
        s =>
          Try(Path.of(s).toFile).filter(_.exists()) match {
            case Success(_) => success
            case Failure(e) => failure(e.getMessage)
        }
      )
      .text("Uber zip path")

    opt[String]('o', "osm")
      .required()
      .valueName("<>")
      .action((o, c) => c.copy(osmMapPath = o))
      .validate(
        o =>
          Try(Path.of(o).toFile).filter(_.exists()) match {
            case Success(_) => success
            case Failure(e) => failure(e.getMessage)
        }
      )
      .text("OSM map file to compare")
  }
}

class SpeedCompareApp extends App with AppSetup {

  parser.parse(args, CompareConfig()) match {
    case Some(conf) => System.exit(0)
    case None       => System.exit(-1)
  }
}
