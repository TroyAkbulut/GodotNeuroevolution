import json

class MockSocket():
    def __init__(self):
        self.recievedMessage = None
        
    def send(self, data):
        self.recievedMessage = json.loads(data.decode())
        
    def recv(self, bufsize):
        return json.dumps(self.recievedMessage).encode()