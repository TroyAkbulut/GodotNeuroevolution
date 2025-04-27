from HelperObjects.GodotConnectionManager import GodotConnectionManager
from HelperObjects.Agent import Agent

class SimulationManager():
    def __init__(self, connection: GodotConnectionManager, agents: list[Agent]):
        self.connection = connection
        self.allAgents = agents
        self.currentAgents = self.allAgents[:]
        self.batchesToRun: list[list[Agent]] = []
        
    def DoSimulation(self) -> None:
        self.connection.Start([agent.agentID for agent in self.currentAgents])

        playersAlive = len(self.currentAgents)
        while playersAlive > 0:
            jsonData = self.connection.GetData(4096+len(self.currentAgents)*100)
            for agentInfo in jsonData["playerInfo"]:
                    agent = Agent.GetAgentByID(agentInfo["playerID"], self.currentAgents)
                    agent.alive = agentInfo["alive"]
                    if agent.alive:
                        inputData: list[int] = jsonData["platformData"][:]
                        agent.SetNextMove(inputData + [agentInfo["x"], agentInfo["y"]])

            agentMovesForGodot: list[dict] = [agent.GetDataForGodot() for agent in self.currentAgents if agent.alive]
            playersAlive = len(agentMovesForGodot)
            
            if playersAlive > 0:
                self.connection.SendData(agentMovesForGodot)
                
            else:
                jsonData = self.connection.Stop(8192)

                for agentScore in jsonData:
                    agent = Agent.GetAgentByID(agentScore["playerID"], self.currentAgents)
                    agent.SetFitness(agentScore["score"])
                    
    def DoManySimulations(self, batchSize: int) -> None:
        self.agentBatches = [self.allAgents[i:i + batchSize] for i in range(0, len(self.allAgents), batchSize)]
        for batch in self.agentBatches:
            self.currentAgents = batch
            self.DoSimulation()
