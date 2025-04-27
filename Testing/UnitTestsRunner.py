import unittest
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style

from UnitTests.test_Agent import AgentTests
from UnitTests.test_SimulationManager import SimulationManagerTests
from UnitTests.test_Message import MessageTests

colorama_init()

def RunAllTests():
    testResults: list[tuple[unittest.TestResult, str]] = []
    
    agentTests = AgentTests()
    testResults.append((agentTests.run(), "AgentTests (UT1)"))
    
    simulationManagerTests = SimulationManagerTests()
    testResults.append((simulationManagerTests.run(), "SimulationManagerTests (UT2, UT3)"))
    
    simulationManagerTests = MessageTests()
    testResults.append((simulationManagerTests.run(), "MessageTests (UT4, UT5)"))
    
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
    