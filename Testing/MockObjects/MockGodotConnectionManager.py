import json
from HelperObjects.Enums import Signals
from HelperObjects.Message import Message

class MockGodotConnectionManager:
    def __init__(self, ip: str, port: int):
        self.startData = []
        self.dataData = None
        self.killNext = False
        
    def Start(self, agentIDs: list[int]) -> None:
        self.startData = agentIDs
        
    def SendData(self, data: list) -> None:
        self.dataData = data
        
    def GetData(self, bufferSize: int) -> dict:
        returnData = {}
        agentInfo = []
        for id in self.startData:
            info = {}
            info["playerID"] = id
            info["x"] = 0
            info["y"] = 0
            info["alive"] = not self.killNext
            agentInfo.append(info)
            
        returnData["playerInfo"] = agentInfo
        returnData["platformData"] = []
        
        self.killNext = not self.killNext
        
        return returnData

    def Stop(self, bufferSize: int) -> dict:
        returnData = []
        for id in self.startData:
            info = {}
            info["playerID"] = id
            info["score"] = 1
            returnData.append(info)
        
        return returnData