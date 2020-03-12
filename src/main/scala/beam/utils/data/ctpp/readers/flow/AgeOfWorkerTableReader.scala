package beam.utils.data.ctpp.readers.flow

import beam.utils.data.ctpp.CTPPParser
import beam.utils.data.ctpp.models.{AgeRange, FlowGeoParser, OD, ResidenceToWorkplaceFlowGeography}
import beam.utils.data.ctpp.readers.BaseTableReader
import beam.utils.data.ctpp.readers.BaseTableReader.{PathToData, Table}

class AgeOfWorkerTableReader(
  pathToData: PathToData,
  val residenceToWorkplaceFlowGeography: ResidenceToWorkplaceFlowGeography
) extends BaseTableReader(
      pathToData,
      Table.AgeOfWorker,
      Some(residenceToWorkplaceFlowGeography.level)
    ) {

  val allowedGeos: Set[ResidenceToWorkplaceFlowGeography] = Set(
    ResidenceToWorkplaceFlowGeography.`State To State`,
    ResidenceToWorkplaceFlowGeography.`State-County To State-County`,
    ResidenceToWorkplaceFlowGeography.`State-County-MCD To State-County-MCD`,
    ResidenceToWorkplaceFlowGeography.`State-Place To State-Place`,
    ResidenceToWorkplaceFlowGeography.`PUMA5 To POWPUMA`,
    ResidenceToWorkplaceFlowGeography.`Metropolitan Statistical Area To Metropolitan Statistical Area`
  )
  require(
    allowedGeos.contains(residenceToWorkplaceFlowGeography),
    s"Can't find '${residenceToWorkplaceFlowGeography}' in allowedGeos: ${allowedGeos}"
  )

  private val lineNumberToAge: Map[Int, AgeRange] = Map(
    2 -> AgeRange(Range.inclusive(16, 17)),
    3 -> AgeRange(Range.inclusive(18, 24)),
    4 -> AgeRange(Range.inclusive(25, 44)),
    5 -> AgeRange(Range.inclusive(45, 59)),
    6 -> AgeRange(Range.inclusive(60, 64)),
    7 -> AgeRange(Range.inclusive(65, 74)),
    8 -> AgeRange(Range.inclusive(75, 100))
  ) // 75 years and over

  def read(): Seq[OD[AgeRange]] = {
    CTPPParser
      .readTable(pathToCsvTable, x => geographyLevelFilter(x))
      .flatMap { entry =>
        val (fromGeoId, toGeoId) = FlowGeoParser.parse(entry.geoId).get
        lineNumberToAge.get(entry.lineNumber).map { ageRange =>
          OD(fromGeoId, toGeoId, ageRange, entry.estimate)
        }
      }
  }
}

object AgeOfWorkerTableReader {

  def main(args: Array[String]): Unit = {
    val rdr =
      new AgeOfWorkerTableReader(
        PathToData("D:/Work/beam/Austin/2012-2016 CTPP documentation/tx/48"),
        ResidenceToWorkplaceFlowGeography.`State To State`
      )
    val readData = rdr.read()
    readData.foreach { od =>
      println(od)
    }
  }
}