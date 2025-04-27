from NEATObjects.Population import Population
from NEATObjects.Genome import Genome
from NEATObjects.Network import Network
from NEATObjects.NewGeneration import NewGeneration
from HelperObjects.Enums import Moves
from HelperObjects import Agent
from HelperObjects.GodotConnectionManager import GodotConnectionManager
from HelperObjects.SimulationManager import SimulationManager
import visualize
import matplotlib.pyplot as plt

POPULATION_SIZE = 300
GENERATIONS = 300
NUM_INPUTS = 1058
NUM_OUTPUTS = len([move for move in Moves])

DELTA_DISJOINT = 2.0
DELTA_WEIGHT = 0.4
DELTA_THRESHOLD = 2
STALE_SPECIES = 10

MUTATE_CONNECTION_CHANCE= 0.25
PERTURB_CHANCE = 0.90
CROSSOVER_CHANCE = 0.75
LINK_MUTATION_CHANCE = 1.99999
NODE_MUTATION_CHANCE = 0.50
BIAS_MUTATION_CHANCE = 0.40
STEP_SIZE = 0.1
DISABLE_MUTATION_CHANCE = 0.4
ENABLE_MUTATION_CHANCE = 0.2

ip = "127.0.0.1"
port = 4242

connection = GodotConnectionManager(ip="127.0.0.1", port=4242)

population = Population(POPULATION_SIZE, DELTA_DISJOINT, DELTA_WEIGHT, DELTA_THRESHOLD)
for i in range(POPULATION_SIZE):
    genome = Genome.BasicGenome(NUM_INPUTS, NUM_OUTPUTS, 
                                PERTURB_CHANCE, MUTATE_CONNECTION_CHANCE, LINK_MUTATION_CHANCE, BIAS_MUTATION_CHANCE, 
                                NODE_MUTATION_CHANCE, ENABLE_MUTATION_CHANCE, DISABLE_MUTATION_CHANCE, STEP_SIZE, 
                                population)
    population.AddToSpecies(genome)

try:
    for generation in range(GENERATIONS):
        print(f"****** Running generation {population.generation} ******")
        
        i = 0
        agents = []
        for genome in population.GetAllGenomes():
            agent = Agent.Agent(i, genome)
            agents.append(agent)
            i += 1
            
        simulationManager = SimulationManager(connection, agents)
        simulationManager.DoManySimulations(25)
        
        NewGeneration(population, CROSSOVER_CHANCE)
except KeyboardInterrupt:
    pass

visualize.plot_stats(population, view=True, filename="NEAT_output/Graphs/feedforward-fitness.svg")
allGenomes = population.GetAllGenomes()
allGenomes.sort(key=lambda genome: genome.fitness, reverse=True)
bestGenome = allGenomes[0]
visualize.draw_net2(bestGenome, True, filename="NEAT_output/Graphs/winner2")