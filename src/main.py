from inputOutput import readInput, writeOutput
from Simulation import Simulation
from solution.Solution import Solution
from solution.coolingSchedule import *
from menus import *

INPUT_FOLDER = "../input/"
OUTPUT_FOLDER = "../output/"

files = {1: 'a.txt', 2: 'b.txt', 3: 'c.txt', 4: 'd.txt', 5: 'e.txt', 6: 'f.txt'}

def runAlgorithm(inputFile, outputFile, algorithmInput):
    (intersections, cars, maxTime, bonusPoints) = readInput(inputFile)
    simulation = Simulation(cars, maxTime, bonusPoints)
    solution = Solution(intersections, simulation)
    solution.removeUnusedStreets()
    solution.setInitialSolution()

    if algorithmInput == 1:
        finalScore = solution.hillClimbingBasicRandom(1)
    elif algorithmInput == 2:
        finalScore = solution.hillClimbingSteepest()
    elif algorithmInput == 3:
        finalScore = solution.simulatedAnnealing(100, 0.85, 10, exponentialCooling)
    elif algorithmInput == 4:
        finalScore = solution.tabuSearch(100, 10)

    solution.show()
    print("Final score = ", finalScore)
    writeOutput(outputFile, solution.intersections)


def program():
    currentMenu = 0
    inputFile = INPUT_FOLDER + 'a.txt'
    outputFile = OUTPUT_FOLDER + "out.txt"

    while currentMenu != -1:
        if currentMenu == 0:  # main menu
            currentMenu = showMainMenu()

        elif currentMenu == 1:
            fileOption = showFilesMenu()
            # if it's 7 go to main menu
            if fileOption == 7:
                currentMenu = 0
            else:
                currentMenu = 2

            inputFile = INPUT_FOLDER + files[fileOption]

        elif currentMenu == 2:
            algorithmInput = showAlgorithmMenu()
            # if it's 6 then choose another file
            if algorithmInput == 6:
                currentMenu = 1
                continue
            elif algorithmInput == 7:
                currentMenu = 0
                continue

            runAlgorithm(inputFile, outputFile, algorithmInput)


if __name__ == "__main__":
    program()
    '''
    inputFile = INPUT_FOLDER + "b.txt"  # input("Select your input file: ")

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
    finalScore = solution.tabuSearch(100, 10)
    solution.show()
    print("Final score = ", finalScore)

    writeOutput(outputFile, solution.intersections)
    '''