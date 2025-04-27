import unittest
import neat
import neat.config
import os
import sys
projectPath = os.path.abspath(os.path.join(os.path.realpath(__file__), "..", "..", ".."))
sys.path.append(projectPath)

from HelperObjects.SimulationManager import SimulationManager
from HelperObjects.Agent import Agent
from HelperObjects.GodotConnectionManager import GodotConnectionManager
from HelperObjects.Enums import Moves
from NEATObjects.Genome import Genome
from NEATObjects.Population import Population

POPULATION_SIZE = 5
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

class SimulationManagerTests(unittest.TestCase):
    connection: GodotConnectionManager = None
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, os.path.join(os.path.realpath(__file__), "..", "testConfig.txt"))
    
    def __init__(self, connection: GodotConnectionManager, methodName = "runTest"):
        super().__init__(methodName)
        self.connection = connection
    
    def runTest(self):
        self.test_DoSimulation()
        self.test_DoManySimulations()
    
    #IT19
    def test_DoSimulation(self):
        if not self.connection:
            self.skipTest("No connection to the Godot server")
        
        libPopulation = neat.Population(self.config)
        libAgents = Agent.CreateAgentsFromGenomes(list(libPopulation.population.items()), self.config)
        
        simulationManager = SimulationManager(self.connection, libAgents)
        simulationManager.DoSimulation()

        for agent in libAgents:
            self.assertEqual(agent.fitness, agent.genome.fitness)
            self.assertNotEqual(agent.fitness, 0)
            
        population = Population(POPULATION_SIZE, DELTA_DISJOINT, DELTA_WEIGHT, DELTA_THRESHOLD)
        neatAgents: list[Agent] = []
        for i in range(POPULATION_SIZE):
            genome = Genome.BasicGenome(NUM_INPUTS, NUM_OUTPUTS, 
                                    PERTURB_CHANCE, MUTATE_CONNECTION_CHANCE, LINK_MUTATION_CHANCE, BIAS_MUTATION_CHANCE, 
                                    NODE_MUTATION_CHANCE, ENABLE_MUTATION_CHANCE, DISABLE_MUTATION_CHANCE, STEP_SIZE, 
                                    population)
            agent = Agent(i, genome)
            neatAgents.append(agent)
            
        simulationManager = SimulationManager(self.connection, neatAgents)
        simulationManager.DoSimulation()

        for agent in neatAgents:
            self.assertEqual(agent.fitness, agent.genome.fitness)
            self.assertNotEqual(agent.fitness, 0)
        
        
    #IT20   
    def test_DoManySimulations(self):
        if not self.connection:
            self.skipTest()
        
        libPopulation = neat.Population(self.config)
        libAgents = Agent.CreateAgentsFromGenomes(list(libPopulation.population.items()), self.config)
        
        simulationManager = SimulationManager(self.connection, libAgents)
        simulationManager.DoManySimulations(2)
        
        for agent in libAgents:
            self.assertEqual(agent.fitness, agent.genome.fitness)
            self.assertNotEqual(agent.fitness, 0)
            
        population = Population(POPULATION_SIZE, DELTA_DISJOINT, DELTA_WEIGHT, DELTA_THRESHOLD)
        neatAgents: list[Agent] = []
        for i in range(POPULATION_SIZE):
            genome = Genome.BasicGenome(NUM_INPUTS, NUM_OUTPUTS, 
                                    PERTURB_CHANCE, MUTATE_CONNECTION_CHANCE, LINK_MUTATION_CHANCE, BIAS_MUTATION_CHANCE, 
                                    NODE_MUTATION_CHANCE, ENABLE_MUTATION_CHANCE, DISABLE_MUTATION_CHANCE, STEP_SIZE, 
                                    population)
            agent = Agent(i, genome)
            neatAgents.append(agent)
            
        simulationManager = SimulationManager(self.connection, neatAgents)
        simulationManager.DoManySimulations(2)
        
        for agent in neatAgents:
            self.assertEqual(agent.fitness, agent.genome.fitness)
            self.assertNotEqual(agent.fitness, 0)
    
if __name__ == '__main__':
    unittest.main()