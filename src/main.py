from inputOutput import readInput, writeOutput
from Simulation import Simulation
from Solution import Solution
from coolingSchedule import *

INPUT_FOLDER = "input/"
OUTPUT_FOLDER = "output/"

if __name__ == "__main__":
    inputFile = INPUT_FOLDER + "e.txt"  # input("Select your input file: ")
    
    outputFile = OUTPUT_FOLDER + "out.txt"  # input("Select your output file: ")

    (intersections, cars, maxTime, bonusPoints) = readInput(inputFile)
    simulation = Simulation(cars, maxTime, bonusPoints)

    solution = Solution(intersections, simulation)
    solution.removeUnusedStreets()
    solution.setInitialSolution()
    # finalScore = solution.hillClimbingBasicRandom(1000)
    # finalScore = solution.hillClimbingSteepest()
    # finalScore = solution.simulatedAnnealing(100, 0.85, 10, exponentialCooling)
    finalScore = solution.tabuSearch(10, 100)
    solution.show()
    print("Final score = ", finalScore)

    writeOutput(outputFile, solution.intersections)
