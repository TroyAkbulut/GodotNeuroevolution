import unittest
import os
import sys
projectPath = os.path.abspath(os.path.join(os.path.realpath(__file__), "..", "..", ".."))
sys.path.append(projectPath)

from HelperObjects.Message import Message
from Testing.MockObjects.MockSocket import MockSocket
from HelperObjects.Enums import Signals

class MessageTests(unittest.TestCase):
    
    def runTest(self):
        self.test_SendMessage()
        self.test_SendAndRecieve()
    
    #UT4
    def test_SendMessage(self):
        testSignal = Signals.TEST
        testData = [1, 2, 3]
        connection = MockSocket()
        message = Message(testSignal, testData)
        
        message.SendMessage(connection)
        
        self.assertEqual(connection.recievedMessage["signal"], testSignal)
        self.assertEqual(connection.recievedMessage["data"], testData)

    #UT5
    def test_SendAndRecieve(self):
        testSignal = Signals.TEST
        testData = [1, 2, 3]
        connection = MockSocket()
        message = Message(testSignal, testData)
        
        returnedMessage = message.SendAndRecieve(connection, 1)
        
        self.assertEqual(connection.recievedMessage["signal"], testSignal)
        self.assertEqual(connection.recievedMessage["data"], testData)
        self.assertEqual(connection.recievedMessage["signal"], returnedMessage["signal"])
        self.assertEqual(connection.recievedMessage["data"], returnedMessage["data"])
    
if __name__ == '__main__':
    unittest.main()