import socket
import json
from HelperObjects.Enums import Signals

class Message:
    def __init__(self, signal: Signals, data):
        self.signal = signal
        self.data = data
        
    def SendMessage(self, connection: socket.socket) -> None:
        connection.send(json.dumps(self.__dict__).encode())
        
    def SendAndRecieve(self, connection: socket.socket, bufferSize: int) -> dict:
        self.SendMessage(connection)
        return json.loads(connection.recv(bufferSize).decode())
