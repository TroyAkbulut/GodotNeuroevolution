import unittest
import os
import sys
import neat
import neat.config
projectPath = os.path.abspath(os.path.join(os.path.realpath(__file__), "..", "..", ".."))
sys.path.append(projectPath)

from HelperObjects.Agent import Agent
from HelperObjects.Enums import Moves
from NEATObjects.Genome import Genome
from NEATObjects.Population import Population
from NEATObjects.Network import Network

POPULATION_SIZE = 300
NUM_INPUTS = 1058
NUM_OUTPUTS = len([move for move in Moves])

DELTA_DISJOINT = 2.0
DELTA_WEIGHT = 0.4
DELTA_THRESHOLD = 3.5

MUTATE_CONNECTION_CHANCE= 0.25
PERTURB_CHANCE = 0.90
LINK_MUTATION_CHANCE = 1.99999
NODE_MUTATION_CHANCE = 0.50
BIAS_MUTATION_CHANCE = 0.40
STEP_SIZE = 0.1
DISABLE_MUTATION_CHANCE = 0.4
ENABLE_MUTATION_CHANCE = 0.2

class AgentTests(unittest.TestCase):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, os.path.join(os.path.realpath(__file__), "..", "testConfig.txt"))
    population = Population(POPULATION_SIZE, DELTA_DISJOINT, DELTA_WEIGHT, DELTA_THRESHOLD)
    
    def runTest(self):
        self.test_AgentCreation()
        self.test_SetNextMove()
        self.test_SetFitness()
    
    #IT16
    def test_AgentCreation(self):
        libGenome = neat.DefaultGenome(1)
        neatGenome = Genome.BasicGenome(NUM_INPUTS, NUM_OUTPUTS, 
                                        PERTURB_CHANCE, MUTATE_CONNECTION_CHANCE, LINK_MUTATION_CHANCE, BIAS_MUTATION_CHANCE, 
                                        NODE_MUTATION_CHANCE, ENABLE_MUTATION_CHANCE, DISABLE_MUTATION_CHANCE, STEP_SIZE, 
                                        self.population)
        
        libAgent = Agent(1, libGenome, self.config)
        neatAgent = Agent(2, neatGenome)
        
        self.assertIsInstance(libAgent.neuralNetwork, neat.nn.RecurrentNetwork)
        self.assertIsInstance(neatAgent.genome.network, Network)
    
    #IT17
    def test_SetNextMove(self):
        libGenome = neat.DefaultGenome(1)
        neatGenome = Genome.BasicGenome(NUM_INPUTS, NUM_OUTPUTS, 
                                        PERTURB_CHANCE, MUTATE_CONNECTION_CHANCE, LINK_MUTATION_CHANCE, BIAS_MUTATION_CHANCE, 
                                        NODE_MUTATION_CHANCE, ENABLE_MUTATION_CHANCE, DISABLE_MUTATION_CHANCE, STEP_SIZE, 
                                        self.population)
        
        libAgent = Agent(1, libGenome, self.config)
        neatAgent = Agent(2, neatGenome)
        
        data = [float(i)/1057 for i in range(1058)]
        libAgent.SetNextMove(data)
        neatAgent.SetNextMove(data)
        
        self.assertTrue(len(libAgent.nextMoves) == 0)
        self.assertTrue(0 <= len(neatAgent.nextMoves) <= 3)
        
        for move in neatAgent.nextMoves:
            self.assertIn(move, Moves._value2member_map_)
    
    #IT18
    def test_SetFitness(self):
        libGenome = neat.DefaultGenome(1)
        neatGenome = Genome.BasicGenome(NUM_INPUTS, NUM_OUTPUTS, 
                                        PERTURB_CHANCE, MUTATE_CONNECTION_CHANCE, LINK_MUTATION_CHANCE, BIAS_MUTATION_CHANCE, 
                                        NODE_MUTATION_CHANCE, ENABLE_MUTATION_CHANCE, DISABLE_MUTATION_CHANCE, STEP_SIZE, 
                                        self.population)
        
        libAgent = Agent(1, libGenome, self.config)
        neatAgent = Agent(2, neatGenome)
        
        libAgent.SetFitness(1)
        neatAgent.SetFitness(1)
        
        self.assertTrue(libAgent.fitness == libAgent.genome.fitness == 1)
        self.assertTrue(neatAgent.fitness == neatAgent.genome.fitness == 1)
    
if __name__ == '__main__':
    tests = AgentTests()
    results = tests.run()
    for result in results.failures:
        print(f"{result[1]}")
    for result in results.errors:
        print(f"{result[1]}")