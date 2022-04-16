from inputOutput import readInput, writeOutput
from Simulation import Simulation
from solution.Solution import Solution
from solution.coolingSchedule import *

INPUT_FOLDER = "input/"
OUTPUT_FOLDER = "output/"

if __name__ == "__main__":
    inputFile = INPUT_FOLDER + "e.txt"  # input("Select your input file: ")

    # input("Select your output file: ")
    outputFile = OUTPUT_FOLDER + "out.txt"

    (intersections, cars, maxTime, bonusPoints) = readInput(inputFile)

    simulation = Simulation(cars, maxTime, bonusPoints)

    solution = Solution(intersections, simulation)
    solution.removeUnusedStreets()
    solution.setInitialSolution()
    # finalScore = solution.hillClimbingBasicRandom(1000)
    # finalScore = solution.hillClimbingSteepest()
    # finalScore = solution.simulatedAnnealing(100, 0.85, 10, exponentialCooling)
    # finalScore = solution.tabuSearch(100, 10)
    finalScore = solution.genetic(10, 20, 1000, 0.2)
    solution.show()
    print("Final score = ", finalScore)

    writeOutput(outputFile, solution.intersections)
