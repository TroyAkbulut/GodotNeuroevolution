import unittest
import multiprocessing
import multiprocessing.context
import os
import sys
projectPath = os.path.abspath(os.path.join(os.path.realpath(__file__), "..", "..", ".."))
sys.path.append(projectPath)

from HelperObjects.GodotConnectionManager import GodotConnectionManager
from HelperObjects.Agent import Agent
from HelperObjects.Enums import Moves

ip="127.0.0.1"
port=4242

class GodotConnectionManagerTests(unittest.TestCase):
    connection: GodotConnectionManager = None
    
    def runTest(self):
        self.test_GetGodotConnection()
        self.test_StartRequestStopSignals()
        self.test_SendData()
    
    #IT13
    def test_GetGodotConnection(self):
        pool = multiprocessing.Pool()
        try:
            self.connection = pool.starmap_async(GodotConnectionManager, [(ip, port)]).get(5)[0]
        except multiprocessing.context.TimeoutError:
            pool.close()
            self.fail("Unable to establish connection with godot")
       
    #IT14     
    def test_StartRequestStopSignals(self):
        if not self.connection:
            self.skipTest("No Connection")
        
        agent = Agent(1)
        self.connection.Start([agent.agentID])
        returnedData = self.connection.GetData(8192)
        finalData = self.connection.Stop(8192)
        
        for platformCell in returnedData["platformData"]:
            self.assertTrue(platformCell == 1 or platformCell == 0)
            
        playerData = returnedData["playerInfo"][0]
        self.assertTrue(0 <= playerData["x"] <= 1)
        self.assertTrue(0 <= playerData["y"] <= 1)
        self.assertEqual(playerData["playerID"], agent.agentID)
        
        self.assertEqual(finalData[0]["playerID"], agent.agentID)
        self.assertEqual(finalData[0]["score"], 0)
        
    #IT15
    def test_SendData(self):
        if not self.connection:
            self.skipTest("No Connection")
        
        agent = Agent(1)
        agent.nextMoves = [Moves.JUMP]
        
        self.connection.Start([agent.agentID])
        initialData = self.connection.GetData(8192)
        self.connection.SendData([agent.GetDataForGodot()])
        secondaryData = self.connection.GetData(8192)
        finalData = self.connection.Stop(8192)
        
        initialPlayerData = initialData["playerInfo"][0]
        secondaryPlayerData = secondaryData["playerInfo"][0]
        self.assertTrue(initialPlayerData["x"] > secondaryPlayerData["x"])
        self.assertTrue(initialPlayerData["y"] < secondaryPlayerData["y"])
        
        self.assertEqual(finalData[0]["playerID"], agent.agentID)
        self.assertEqual(finalData[0]["score"], 0)
    
    
if __name__ == '__main__':
    tests = GodotConnectionManagerTests()
    results = tests.run()
    for result in results.failures:
        print(f"{result[1]}")
    for result in results.errors:
        print(f"{result[1]}")