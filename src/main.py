from inputOutput import readInput, writeOutput
from Simulation import Simulation
from Solution import Solution

INPUT_FOLDER = "../input/"
OUTPUT_FOLDER = "../output/"

if __name__ == "__main__":
    inputFile = INPUT_FOLDER + "a.txt"# input("Select your input file: ")
    outputFile = OUTPUT_FOLDER + "out.txt"# input("Select your output file: ")

    (intersections, cars, maxTime, bonusPoints) = readInput(inputFile)
    simulation = Simulation(cars, maxTime, bonusPoints)

    solution = Solution(intersections, simulation)
    solution.removeUnusedStreets()
    solution.setInitialSolution()
    # finalScore = solution.hillClimbingBasicRandom(1000)
    solution.show()
    # print("Final score = ", finalScore)
    print("score after final = ", simulation.eval(solution.intersections))
    print("score after final = ", simulation.eval(solution.intersections))
    print("score after final = ", simulation.eval(solution.intersections))

    writeOutput(outputFile, solution.intersections)

