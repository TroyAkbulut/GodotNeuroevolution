from HelperObjects.Enums import Moves
from NEATObjects.Genome import Genome
from NEATObjects.Species import Species

class Population():
    def __init__(self, populationSize, deltaDisjoint, deltaWeights, deltaThreshold):
            self.species: list[Species] = []
            self.populationSize = populationSize
            self.generation = 0
            self.innovation = len([move for move in Moves])
            self.maxFitness = 0
            self.deltaDisjoint = deltaDisjoint
            self.deltaWeights = deltaWeights
            self.deltaThreshold = deltaThreshold
            
            self.history: dict[str, list[float]] = {}
            self.history["maxFitness"] = []
            self.history["averageFitness"] = []
            self.history["standardDeviation"] = []
            
    def AddToSpecies(self, child: Genome):
        foundSpecies = False
        for species in self.species:
            if not foundSpecies and len(species.genomes) > 0 and Species.SameSpecies(child, species.genomes[0], self.deltaDisjoint, self.deltaWeights, self.deltaThreshold):
                species.genomes.append(child)
                foundSpecies = True
        
        if not foundSpecies:
            childSpecies = Species()
            childSpecies.genomes.append(child)
            self.species.append(childSpecies)
            
    def GetAllGenomes(self) -> list[Genome]:
        genomes = []
        for species in self.species:
            genomes += species.genomes
            
        return genomes
    
    def RecordFitnessAndDeviation(self):
        totalFitness = 0
        genomes = self.GetAllGenomes()
        for genome in genomes:
            totalFitness += genome.fitness
        averageFitness = totalFitness/len(genomes)
        self.history["averageFitness"].append(averageFitness)
        
        totalDeviation = 0
        for genome in genomes:
            totalDeviation += (genome.fitness - averageFitness)**2
        variance = totalDeviation/len(genomes)
        standardDeviation = variance**0.5
        self.history["standardDeviation"].append(standardDeviation)

    def SetMaxFitness(self, maxFitness):
        self.maxFitness = maxFitness
        self.history["maxFitness"].append(maxFitness)