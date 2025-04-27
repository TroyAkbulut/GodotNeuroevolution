from HelperObjects.Agent import Agent
from HelperObjects.GodotConnectionManager import GodotConnectionManager
from HelperObjects.SimulationManager import SimulationManager
import neat.config
import pickle
import visualize

connection = GodotConnectionManager(ip="127.0.0.1", port=4242)
settings = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, "config.txt")
population = neat.Population(settings)

def fitnessFunc(genomes, config):
    agents = Agent.CreateAgentsFromGenomes(genomes, config)
    simulation = SimulationManager(connection, agents)
    simulation.DoManySimulations(50)
        

stats = neat.StatisticsReporter()
checkpointer = neat.Checkpointer(generation_interval=10, time_interval_seconds=None, filename_prefix="NEAT_output/Checkpoints/SavedCheckpoint")
#population = checkpointer.restore_checkpoint("NEAT_output/Checkpoints/SavedCheckpoint99")
population.add_reporter(stats)
population.add_reporter(neat.StdOutReporter(True))
population.add_reporter(checkpointer)

try:
    population.run(fitnessFunc, 200)
except KeyboardInterrupt as e:
    pass
with open('NEAT_output/Genomes/winner', 'wb') as f:
        pickle.dump(population.best_genome, f)

visualize.plot_stats(stats, view=True, filename="NEAT_output/Graphs/feedforward-fitness.svg")
visualize.plot_species(stats, view=True, filename="NEAT_output/Graphs/feedforward-speciation.svg")

visualize.draw_net(settings, population.best_genome, True, prune_unused=True, filename="NEAT_output/Graphs/winner")

