from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from NEATObjects.Population import Population
    
from NEATObjects.Gene import Gene
from NEATObjects.Genome import Genome
from NEATObjects.Mutate import Mutate
import random

class Species():
    def __init__(self):
        self.topFitness = 0
        self.staleness = 0
        self.genomes: list[Genome] = []
        self.averageRank = 0
        
    @staticmethod
    def SameSpecies(genome1: Genome, genome2: Genome, deltaDisjoint, deltaWeights, deltaThreshold) -> bool:
        dd = deltaDisjoint*Species.Disjoint(genome1.genes, genome2.genes)
        dw = deltaWeights*Species.Weights(genome1.genes, genome2.genes)
        return (dd + dw) < deltaThreshold
    
    @staticmethod
    def Disjoint(genes1: list[Gene], genes2: list[Gene]) -> float:
        i1 = {}
        for gene in genes1:
            i1[gene.innovation] = True
            
        i2 = {}
        for gene in genes2:
            i2[gene.innovation] = True
            
        disjointGenes = 0
        for gene in genes1:
            if not gene.innovation in i2:
                disjointGenes += 1
                
        for gene in genes2:
            if not gene.innovation in i1:
                disjointGenes += 1
                
        n = max(len(genes1), len(genes2))
        return disjointGenes/n if n > 0 else 0
        
    @staticmethod
    def Weights(genes1: list[Gene], genes2: list[Gene]) -> float:
        i2 = {}
        for gene in genes2:
            i2[gene.innovation] = gene
            
        sum = 0
        coincident = 0
        for gene in genes1:
            if gene.innovation in i2:
                gene2 = i2[gene.innovation]
                sum = sum + abs(gene.weight - gene2.weight)
                coincident += 1
                
        return sum/coincident if coincident > 0 else 0
    
    def CalculateAverageRank(self):
        total = 0
        for genome in self.genomes:
            total += genome.globalRank
        
        self.averageRank = total/len(self.genomes)
        
    def CrossOver(self, g1: Genome, g2: Genome) -> Genome:
        if g2.fitness > g1.fitness:
            temp = g1
            g1 = g2
            g2 = g1
            
        child = g1.CopyGenome()
        child.genes = []
        
        innovations2 = {}
        for gene in g2.genes:
            innovations2[gene.innovation] = gene
            
        for gene in g1.genes:
            gene2: Gene = innovations2[gene.innovation] if gene.innovation in innovations2 else None
            if gene2 and random.getrandbits(1) and gene2.enabled:
                child.genes.append(gene2.CopyGene())
            else:
                child.genes.append(gene.CopyGene())
                
        child.maxNeuron = max(g1.maxNeuron, g2.maxNeuron)
        return child
        
    def BreedChild(self, crossoverChance: float, population: 'Population') -> Genome:
        child: Genome = None
        if random.random() < crossoverChance:
            g1 = random.choice(self.genomes)
            g2 = random.choice(self.genomes)
            child = self.CrossOver(g1, g2)
        
        else:
            g = random.choice(self.genomes)
            child = g.CopyGenome()
        
        Mutate(child, population)
        return child
