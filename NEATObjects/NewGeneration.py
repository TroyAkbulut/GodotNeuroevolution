from NEATObjects.Population import Population
from NEATObjects.Genome import Genome
import math
import random


def CullSpecies(population: Population, cutToOne: bool):
    for species in population.species:
        species.genomes.sort(key=lambda genome: genome.fitness, reverse=True)
        remaining = math.ceil(len(species.genomes)/2)
        if cutToOne:
            remaining = 1
        
        while len(species.genomes) > remaining:
            species.genomes.pop()
            
def RankGlobally(population: Population) -> Genome:
    allGenomes = population.GetAllGenomes()
    allGenomes.sort(key=lambda genome: genome.fitness, reverse=True)
    for i in range(len(allGenomes)):
        allGenomes[i].globalRank = i
        
    return allGenomes[0]

def RemoveStaleSpecies(population: Population, staleThreshold):
    survived = []
    for species in population.species:
        species.genomes.sort(key=lambda genome: genome.fitness, reverse=True)
        if species.genomes[0].fitness > species.topFitness:
            species.topFitness = species.genomes[0].fitness
            species.staleness = 0
        else:
            species.staleness += 1
            
        if species.staleness < staleThreshold or species.topFitness >= population.maxFitness:
            survived.append(species)
            
    population.species = survived

def totalAverageRank(population: Population):
    total = 0
    for species in population.species:
        total += species.averageRank
        
    return total

def RemoveWeakSpecies(population: Population):
    survived = []
    sum = totalAverageRank(population)
    for species in population.species:
        #breed = math.floor(species.averageRank/sum*population.populationSize)
        if species.averageRank <= (population.populationSize/2) / 2:
            survived.append(species)
        
    if len(survived) <= 0:
        survived += [species for species in population.species if species.topFitness >= population.maxFitness]
        
    population.species = survived

def NewGeneration(population: Population, crossoverChance: float):
    population.RecordFitnessAndDeviation()
    CullSpecies(population, False)
    RankGlobally(population)
    RemoveStaleSpecies(population, 15)
    bestGenome = RankGlobally(population)
    population.SetMaxFitness(bestGenome.fitness)
    
    for species in population.species:
        species.CalculateAverageRank()
        
    RemoveWeakSpecies(population)
    sum = totalAverageRank(population)
    children = []
    for species in population.species:
        breed = math.floor(species.averageRank/sum*population.populationSize) if sum > 0 else 0
        for i in range(breed):
            children.append(species.BreedChild(crossoverChance, population))
            
    CullSpecies(population, True)
    while len(children)+len(population.species) < population.populationSize:
        species = random.choice(population.species)
        children.append(species.BreedChild(crossoverChance, population))
        
    for child in children:
        population.AddToSpecies(child)
        
    population.generation += 1

    print(f"Generation concluded\nBest fitness: {bestGenome.fitness}\nAverage fitness: {population.history['averageFitness'][-1]}\nSpecies: {len(population.species)}\nSpecies Fitnesses{[species.topFitness for species in population.species]}")