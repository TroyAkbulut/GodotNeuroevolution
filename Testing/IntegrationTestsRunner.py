import unittest
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style

from IntegrationTests.test_GodotConnectionManager import GodotConnectionManagerTests
from IntegrationTests.test_GodotTests import GodotTests
from IntegrationTests.test_Agent import AgentTests
from IntegrationTests.test_SimulationManager import SimulationManagerTests

def RunAllTests():
    testResults: list[tuple[unittest.TestResult, str]] = []
    
    agentTests = AgentTests()
    testResults.append((agentTests.run(), "AgentTests (IT16, IT17, IT18)"))
    
    godotConnectionManagerTests = GodotConnectionManagerTests()
    testResults.append((godotConnectionManagerTests.run(), "GodotConnectionManagerTests (IT13, IT14, IT15)"))
    connection = godotConnectionManagerTests.connection
    
    simulationManagerTests = SimulationManagerTests(connection)
    testResults.append((simulationManagerTests.run(), "SimulationManagerTests (IT19, IT20)"))
    
    godotTests = GodotTests(connection)
    testResults.append((godotTests.run(), "GodotTests (IT1-12)"))
    
    for results in testResults:
        print(f"Results for {results[1]}:")
        print(f"\tFailures={len(results[0].failures)}, Errors={len(results[0].errors)}")
        
        if results[0].wasSuccessful():
            print(f"\t{Fore.GREEN}All tests passing{Style.RESET_ALL}")
        
        for result in results[0].failures:
            print(f"{Fore.RED}{result[1]}{Style.RESET_ALL}")
        for result in results[0].errors:
            print(f"{Fore.RED}{result[1]}{Style.RESET_ALL}")
    
    
if __name__ == "__main__":
    RunAllTests()
    