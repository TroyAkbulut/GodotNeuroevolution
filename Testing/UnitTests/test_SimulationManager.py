import unittest
import os
import sys
projectPath = os.path.abspath(os.path.join(os.path.realpath(__file__), "..", "..", ".."))
sys.path.append(projectPath)

from HelperObjects.SimulationManager import SimulationManager
from HelperObjects.Enums import Moves
from Testing.MockObjects.MockAgent import MockAgent
from Testing.MockObjects.MockGodotConnectionManager import MockGodotConnectionManager

class SimulationManagerTests(unittest.TestCase):
    
    def runTest(self):
        self.test_DoSimulation()
        self.test_DoManySimulation()
    
    #UT2
    def test_DoSimulation(self):
        connectionManager = MockGodotConnectionManager(None, None)
        agents = []
        agentIDs = []
        for i in range(10):
            agents.append(MockAgent(i))
            agentIDs.append(i)
        
        simulationManager = SimulationManager(connectionManager, agents)
        simulationManager.DoSimulation()
        self.assertEqual(connectionManager.startData, agentIDs)
        for agentData in connectionManager.dataData:
            agent = MockAgent.GetAgentByID(agentData["agentID"], agents)
            self.assertEqual(agentData["moves"], [Moves.RIGHT])
            self.assertEqual(agentData["moves"], agent.nextMoves)
        
    #UT3    
    def test_DoManySimulation(self):
        connectionManager = MockGodotConnectionManager(None, None)
        agents = []
        agentIDs = []
        for i in range(10):
            agents.append(MockAgent(i))
            agentIDs.append(i)
        
        simulationManager = SimulationManager(connectionManager, agents)
        simulationManager.DoManySimulations(5)
        for agent in agents:
            self.assertEqual(agent.nextMoves, [Moves.RIGHT])
    
if __name__ == '__main__':
    unittest.main()