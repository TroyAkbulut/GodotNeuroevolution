from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from NEATObjects.Genome import Genome
    from NEATObjects.Population import Population
    
from NEATObjects.Gene import Gene
from NEATObjects.Network import MAX_NODES
import random


def PointMutate(genome: 'Genome'):
    step = genome.mutationRates["step"]
    
    for gene in genome.genes:
        if random.random() < genome.mutationRates["connections"]:
            gene.weight = gene.weight + random.random()*step*2 - step

def RandomNeuron(genome: 'Genome', nonInput):
    neurons = {}
    if not nonInput:
        for i in range(genome.numInputs):
            neurons[i] = True
            
    for o in range(genome.numOutputs):
        neurons[MAX_NODES+o] = True
        
    for gene in genome.genes:
        if not hasattr(gene, "into"):
            gene.into = 0
            
        if (not nonInput) or gene.into > genome.numInputs:
            neurons[gene.into] = True
        
        if (not nonInput) or gene.out > genome.numInputs:
            neurons[gene.out] = True
            
    n = random.randint(0, len(neurons))
    for key, value in neurons.items():
        if n == 0:
            return key
        n -= 1
    
    return 0

def ContainsLink(genes: list[Gene], link: Gene):
    for gene in genes:
        if gene.into == link.into and gene.out == link.out:
            return True

def NewInnovation(population: 'Population'):
    population.innovation += 1
    return population.innovation

def LinkMutate(genome: 'Genome', population: 'Population', forceBias: bool):
    neuron1 = RandomNeuron(genome, False)
    neuron2 = RandomNeuron(genome, True)
    
    newLink = Gene()
    if neuron1 <= genome.numInputs and neuron2 <= genome.numInputs:
        LinkMutate(genome, population, forceBias)
        return
    
    if neuron2 <= genome.numInputs:
        temp = neuron1
        neuron1 = neuron2
        neuron2 = temp
        
    newLink.into = neuron1
    newLink.out = neuron2
    
    if forceBias:
        newLink.into = genome.numInputs
        
    if ContainsLink(genome.genes, newLink) and not forceBias:
        LinkMutate(genome, population, forceBias)
        return
    
    newLink.innovation = NewInnovation(population)
    newLink.weight = random.random()*4-2
    genome.genes.append(newLink)
            
def NodeMutate(genome: 'Genome', population: 'Population'):
    if len(genome.genes) == 0:
        return
    
    genome.maxNeuron = genome.maxNeuron + 1
    gene = random.choice([gene for gene in genome.genes if gene.enabled])
    
    gene.enabled = False
    
    newGene1 = gene.CopyGene()
    newGene1.out = genome.maxNeuron
    newGene1.weight = 1.0
    newGene1.innovation = NewInnovation(population)
    newGene1.enabled = True
    genome.genes.append(newGene1)
    
    newGene2 = gene.CopyGene()
    newGene2.into = genome.maxNeuron
    newGene2.innovation = NewInnovation(population)
    newGene2.enabled = True
    genome.genes.append(newGene2)
    
def EnableDisableMutate(genome: 'Genome', enable: bool):
    candidates: list[Gene] = []
    for gene in genome.genes:
        if gene.enabled != enable:
            candidates.append(gene)
            
    if len(candidates) == 0:
        return

    chosenGene = random.choice(candidates)
    chosenGene.enabled = not gene.enabled
            
def Mutate(genome: 'Genome', population: 'Population'):
    PointMutate(genome)
        
    p = genome.mutationRates["link"]
    attempts = int(p // 1) + 1
    for i in range(attempts):
        if random.random() < p + 1 - attempts:
            LinkMutate(genome, population, False)
        
    p = genome.mutationRates["bias"]
    attempts = int(p // 1) + 1
    for i in range(attempts):
        if random.random() < p + 1 - attempts:
            LinkMutate(genome, population, True)
        
    p = genome.mutationRates["node"]
    attempts = int(p // 1) + 1
    for i in range(attempts):
        if random.random() < p + 1 - attempts:
            NodeMutate(genome, population)
    
    p = genome.mutationRates["enable"]
    attempts = int(p // 1) + 1
    for i in range(attempts):
        if random.random() < p + 1 - attempts:
            EnableDisableMutate(genome, True)
        
    p = genome.mutationRates["disable"]
    attempts = int(p // 1) + 1
    for i in range(attempts):
        if random.random() < p + 1 - attempts:
            EnableDisableMutate(genome, False)