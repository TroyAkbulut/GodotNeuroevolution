from __future__ import annotations
import os
import sys
projectPath = os.path.abspath(os.path.join(os.path.realpath(__file__), "..", "..", ".."))
sys.path.append(projectPath)

from HelperObjects.Enums import Moves

class MockAgent():
    def __init__(self, agentID:int=-1, genome= None, config = None):
        self.agentID = agentID
        self.genome = genome
        
        self.alive: bool = True
        self.fitness: float = 0
        
        self.nextMoves: list[Moves] = [Moves.LEFT]
            
    @staticmethod
    def GetAgentByID(agentID: int, agentList: list[MockAgent]) -> MockAgent:
        return [agent for agent in agentList if agent.agentID == agentID][0]    
        
    def SetNextMove(self, inputData: list[int]):
        self.nextMoves = [Moves.RIGHT]
        
    def SetFitness(self, fitness: float):
        self.fitness = fitness

    def GetDataForGodot(self) -> dict:
        data = dict()
        data["agentID"] = self.agentID
        data["moves"] = self.nextMoves
        return data
            