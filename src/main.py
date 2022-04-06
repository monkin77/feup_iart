from inputOutput import readInput, writeOutput
from Simulation import Simulation
from Solution import Solution

INPUT_FOLDER = "../input/"
OUTPUT_FOLDER = "../output/"

if __name__ == "__main__":
    inputFile = INPUT_FOLDER + input("Select your input file: ")
    outputFile = OUTPUT_FOLDER + input("Select your output file: ")

    (intersections, cars, maxTime, bonusPoints) = readInput(inputFile)

    solution = Solution(intersections)
    solution.removeUnusedStreets()
    simulation = Simulation(intersections, cars, maxTime, bonusPoints)
    result = simulation.eval()
    print("Total evaluation:", result)

    writeOutput(outputFile, intersections)

