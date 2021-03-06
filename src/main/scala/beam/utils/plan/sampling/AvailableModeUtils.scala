package beam.utils.plan.sampling

import java.util

import beam.router.Modes.BeamMode
import beam.sim.BeamScenario
import beam.sim.population.{AttributesOfIndividual, PopulationAdjustment}
import com.typesafe.scalalogging.LazyLogging
import org.matsim.api.core.v01.population.{Person, Plan, Population}
import org.matsim.core.population.algorithms.PermissibleModesCalculator
import org.matsim.households.Household

import scala.collection.JavaConverters

/**
  * Several utility/convenience methods for mode availability. Note that the MATSim convention
  * is to call these permissible modes. BEAM uses available modes. The semantics are identical.
  */
object AvailableModeUtils extends LazyLogging {

  object AllowAllModes extends PermissibleModesCalculator {
    override def getPermissibleModes(plan: Plan): util.Collection[String] = {
      JavaConverters.asJavaCollection(BeamMode.allModes.map(_.toString))
    }
  }

  def availableModeParser(availableModes: String): Seq[BeamMode] = {
    availableModes.split(",").toSeq map BeamMode.withValue
  }

  /**
    * Gets the excluded modes set for the given person in the population
    *
    * @param population population from the scenario
    * @param personId the respective person's id
    * @return List of excluded mode string
    */
  def getExcludedModesForPerson(population: Population, personId: String): Array[String] = {
    Option(
      population.getPersonAttributes.getAttribute(personId, PopulationAdjustment.EXCLUDED_MODES)
    ).map(_.toString) match {
      case Some(modes) =>
        if (modes.isEmpty) {
          Array.empty[String]
        } else {
          modes.split(",")
        }
      case None => Array.empty[String]
    }
  }

  /**
    * Gets the excluded modes set for the given person
    *
    * @param person the respective person
    * @return
    */
  def availableModesForPerson(person: Person): Seq[BeamMode] = getPersonCustomAttributes(person).availableModes

  /**
    * Sets the available modes for the given person in the population
    *
    * @param population population from the scenario
    * @param person the respective person
    * @param permissibleModes List of permissible modes for the person
    */
  def setAvailableModesForPerson(person: Person, population: Population, permissibleModes: Seq[String]): Unit = {
    val attributesOfIndividual = getPersonCustomAttributes(person)
    setModesForPerson(person, population, permissibleModes, attributesOfIndividual)
  }

  private def setModesForPerson(
    person: Person,
    population: Population,
    permissibleModes: Seq[String],
    attributesOfIndividual: AttributesOfIndividual
  ): Unit = {
    val availableModes = getAvailableModesOfPerson(person, population, permissibleModes)
    try {
      val attributesUpdated =
        attributesOfIndividual.copy(availableModes = availableModes.map(f => BeamMode.withValue(f.toLowerCase)))
      person.getCustomAttributes.put(PopulationAdjustment.BEAM_ATTRIBUTES, attributesUpdated)
    } catch {
      case e: Exception =>
        logger.error("Error while converting available mode string to respective Beam Mode Enums : " + e.getMessage, e)
    }
  }

  private def getAvailableModesOfPerson(
    person: Person,
    population: Population,
    permissibleModes: Seq[String]
  ): Seq[String] = {
    val excludedModes = getExcludedModesForPerson(population, person.getId.toString)
    permissibleModes.filterNot(am => excludedModes.exists(em => em.equalsIgnoreCase(am)))
  }

  def setAvailableModesForPerson_v2(
    beamScenario: BeamScenario,
    person: Person,
    household: Household,
    population: Population,
    permissibleModes: Seq[String]
  ): Unit = {
    val attributesOfIndividual = getOrElseUpdateAttributesOfIndividual(beamScenario, person, household, population)
    setModesForPerson(person, population, permissibleModes, attributesOfIndividual)
  }

  private def getOrElseUpdateAttributesOfIndividual(
    beamScenario: BeamScenario,
    person: Person,
    household: Household,
    population: Population
  ): AttributesOfIndividual = {
    Option(getPersonCustomAttributes(person)).getOrElse {
      val attribs: AttributesOfIndividual =
        PopulationAdjustment.createAttributesOfIndividual(beamScenario, population, person, household)
      person.getCustomAttributes.put(PopulationAdjustment.BEAM_ATTRIBUTES, attribs)
      attribs
    }
  }

  private def getPersonCustomAttributes(person: Person): AttributesOfIndividual = {
    person.getCustomAttributes
      .get(PopulationAdjustment.BEAM_ATTRIBUTES)
      .asInstanceOf[AttributesOfIndividual]
  }

  /**
    * Replaces the available modes given with the existing available modes for the given person
    *
    * @param person the respective person
    * @param newAvailableModes List of new available modes to replace
    */
  def replaceAvailableModesForPerson(person: Person, newAvailableModes: Seq[String]): Unit = {
    val attributesOfIndividual = getPersonCustomAttributes(person)
    try {
      person.getCustomAttributes
        .put(
          PopulationAdjustment.BEAM_ATTRIBUTES,
          attributesOfIndividual.copy(availableModes = newAvailableModes.map(f => BeamMode.withValue(f.toLowerCase)))
        )
    } catch {
      case e: Exception =>
        logger.error("Error while converting available mode string to respective Beam Mode Enums : " + e.getMessage, e)
    }
  }

}
