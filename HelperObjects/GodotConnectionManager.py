import socket
import time
from HelperObjects.Enums import Signals
from HelperObjects.Message import Message

class GodotConnectionManager:
    def __init__(self, ip: str, port: int):
        while True:
            self.connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.message = Message(None, None)
            self.connection.connect((ip, port))
            self.connection.send("Python Socket Connected".encode())
            try:
                print(self.connection.recv(4096))
                break
            except ConnectionResetError:
                time.sleep(1)
                print("Connection failed, retrying...")
                continue
        
    def Start(self, agentIDs: list[int]) -> None:
        self.message.signal = Signals.START
        self.message.data = agentIDs
        self.message.SendMessage(self.connection)
        
    def SendData(self, data: list) -> None:
        self.message.signal = Signals.DATA
        self.message.data = data
        self.message.SendMessage(self.connection)
        
    def GetData(self, bufferSize: int) -> dict:
        self.message.signal = Signals.REQUEST
        self.message.data = None
        return self.message.SendAndRecieve(self.connection, bufferSize)

    def Stop(self, bufferSize: int) -> dict:
        self.message.signal = Signals.STOP
        self.message.data = None
        return self.message.SendAndRecieve(self.connection, bufferSize)
    
    def Test(self) -> None:
        self.message.signal = Signals.TEST
        self.message.data = None
        self.message.SendMessage(self.connection)