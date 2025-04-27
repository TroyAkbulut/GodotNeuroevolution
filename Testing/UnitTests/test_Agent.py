import unittest
import os
import sys
projectPath = os.path.abspath(os.path.join(os.path.realpath(__file__), "..", "..", ".."))
sys.path.append(projectPath)

from HelperObjects.Agent import Agent
from HelperObjects.Enums import Moves

class AgentTests(unittest.TestCase):
    def runTest(self):
        self.test_GetAgentDataForGodot()
    
    #UT1
    def test_GetAgentDataForGodot(self):
        agent = Agent(1, None, None)
        agent.nextMoves = [Moves.RIGHT]
        
        agentData = agent.GetDataForGodot()
        
        self.assertEqual(agentData["agentID"], 1)
        self.assertEqual(agentData["moves"], [Moves.RIGHT])
    
if __name__ == '__main__':
    tests = AgentTests()
    results = tests.run()
    for result in results.failures:
        print(f"{result[1]}")
    for result in results.errors:
        print(f"{result[1]}")