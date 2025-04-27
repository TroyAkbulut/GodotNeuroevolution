from __future__ import annotations
from NEATObjects.Gene import Gene
from NEATObjects.Mutate import Mutate
from NEATObjects.Network import Network
import random


class Genome():
    def __init__(self, numInputs, numOutputs, 
                 perturbChance, mutateConnectionsChance, linkMutationChance, biasMutationChance, nodeMutationChance, enableMutationChance, disableMutationChance, stepSize):
        self.genes: list[Gene] = []
        self.fitness = 0
        self.adjustedFitness = 0
        self.network: Network = None
        self.numInputs = numInputs
        self.numOutputs = numOutputs
        self.maxNeuron = 0
        self.globalRank = 0
        self.mutationRates: dict[str, float] = {}
        
        self.perturbChance = perturbChance
        self.mutationRates["connections"] = mutateConnectionsChance
        self.mutationRates["link"] = linkMutationChance
        self.mutationRates["bias"] = biasMutationChance
        self.mutationRates["node"] = nodeMutationChance
        self.mutationRates["enable"] = enableMutationChance
        self.mutationRates["disable"] = disableMutationChance
        self.mutationRates["step"] = stepSize
        
    @staticmethod
    def BasicGenome(numInputs, numOutputs, 
                    perturbChance, mutateConnectionsChance, linkMutationChance, biasMutationChance, nodeMutationChance, enableMutationChance, disableMutationChance, stepSize, 
                    population) -> Genome:
        genome = Genome(numInputs, 
                        numOutputs, 
                        perturbChance, 
                        mutateConnectionsChance, 
                        linkMutationChance, 
                        biasMutationChance, 
                        nodeMutationChance, 
                        enableMutationChance, 
                        disableMutationChance, 
                        stepSize)

        genome.maxNeuron = numInputs
        Mutate(genome, population)
        
        return genome

    def CopyGenome(self) -> Genome:
        newGenome = Genome(self.numInputs,
                           self.numOutputs,
                           self.perturbChance,
                           self.mutationRates["connections"], 
                           self.mutationRates["link"], 
                           self.mutationRates["bias"], 
                           self.mutationRates["node"], 
                           self.mutationRates["enable"], 
                           self.mutationRates["disable"], 
                           self.mutationRates["step"])
        
        for gene in self.genes:
            newGenome.genes.append(gene.CopyGene())
            
        newGenome.maxNeuron = self.maxNeuron
        return newGenome
