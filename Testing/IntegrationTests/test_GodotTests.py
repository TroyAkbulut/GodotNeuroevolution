import unittest
import os
import sys
projectPath = os.path.abspath(os.path.join(os.path.realpath(__file__), "..", "..", ".."))
sys.path.append(projectPath)

from HelperObjects.GodotConnectionManager import GodotConnectionManager

ip="127.0.0.1"
port=4242

class GodotTests(unittest.TestCase):
    connection: GodotConnectionManager = None
    
    def __init__(self, connection: GodotConnectionManager, methodName = "runTest"):
        super().__init__(methodName)
        self.connection = connection
    
    def runTest(self):
        self.test_GodotTests()
        
    def test_GodotTests(self):
        if not self.connection:
            self.skipTest("No connection to godot")
            
        self.connection.Test()
    
    
if __name__ == '__main__':
    tests = GodotTests()
    results = tests.run()
    for result in results.failures:
        print(f"{result[1]}")
    for result in results.errors:
        print(f"{result[1]}")