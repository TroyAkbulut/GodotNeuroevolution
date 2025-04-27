from __future__ import annotations
import neat.config
import neat.genome
import neat.nn
from NEATObjects.Genome import Genome
from NEATObjects.Network import Network
from HelperObjects.Enums import Moves

class Agent():
    def __init__(self, agentID:int=-1, genome: neat.genome.DefaultGenome | Genome = None, config: neat.config.Config | None = None):
        self.agentID = agentID
        self.genome = genome
        
        self.alive: bool = True
        self.fitness: float = 0
        
        self.nextMoves: list[Moves] = []
        
        if genome:
            self.genome.fitness = 0
            
            if type(genome) == neat.genome.DefaultGenome:
                self.neuralNetwork = neat.nn.RecurrentNetwork.create(genome, config)
                
            if type(genome) == Genome:
                genome.network = Network(genome)
            
    @staticmethod
    def CreateAgentsFromGenomes(genomes: list[neat.genome.DefaultGenome] = None, config: neat.config.Config | None = None) -> list[Agent]:
        agents: list[Agent] = []
        for genomeId, genome in genomes:
            agent = Agent(genomeId, genome, config)
            agents.append(agent)
            
        return agents
            
    @staticmethod
    def GetAgentByID(agentID: int, agentList: list[Agent]) -> Agent:
        return [agent for agent in agentList if agent.agentID == agentID][0]    
        
    def SetNextMove(self, inputData: list[int]):
        if type(self.genome) == neat.genome.DefaultGenome:
            outputs = self.neuralNetwork.activate(inputData)
            self.nextMoves = [outputs.index(output) for output in outputs if output > 0.5]
        elif type(self.genome) == Genome:
            outputs = self.genome.network.GetOutputs(inputData, self.genome.numInputs, self.genome.numOutputs, 0.5)
            self.nextMoves = [output for output in outputs if outputs[output]]
        
    def SetFitness(self, fitness: float):
        self.fitness = fitness
        self.genome.fitness = fitness

    def GetDataForGodot(self) -> dict:
        data = dict()
        data["agentID"] = self.agentID
        data["moves"] = self.nextMoves
        return data
            