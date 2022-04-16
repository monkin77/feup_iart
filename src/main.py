from inputOutput import readInput, writeOutput
from Simulation import Simulation
from solution.Solution import Solution
from solution.coolingSchedule import *
from menus import *

INPUT_FOLDER = "../input/"
OUTPUT_FOLDER = "../output/"

files = {1: 'a.txt', 2: 'b.txt', 3: 'c.txt', 4: 'd.txt', 5: 'e.txt', 6: 'f.txt'}
flags = {'removeUnusedStreets': False, 'iterations': 0, 'inicialTemperature': 100, 'alpha': 0.85, 'precision': 10, 'tabuNumCandidates': 10}

def runAlgorithm(inputFile, outputFile, algorithmInput, flags):
    (intersections, cars, maxTime, bonusPoints) = readInput(inputFile)
    simulation = Simulation(cars, maxTime, bonusPoints)
    solution = Solution(intersections, simulation)

    if flags['removeUnusedStreets']:
        solution.removeUnusedStreets()

    solution.setInitialSolution()

    if algorithmInput == 1:
        finalScore = solution.hillClimbingBasicRandom(flags['iterations'])
    elif algorithmInput == 2:
        finalScore = solution.hillClimbingSteepest()
    elif algorithmInput == 3:
        finalScore = solution.simulatedAnnealing(flags['inicialTemperature'], flags['alpha'], flags['precision'], exponentialCooling)
    elif algorithmInput == 4:
        finalScore = solution.tabuSearch(flags['iterations'], flags['tabuNumCandidates'])

    solution.show()
    print("Final score = ", finalScore)
    writeOutput(outputFile, solution.intersections)


def program():
    currentMenu = 0
    inputFile = INPUT_FOLDER + 'a.txt'
    outputFile = OUTPUT_FOLDER + "out.txt"
    currFlags = flags

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
            configInput = getInitialConfig()
            userInput = True
            # choose algorithm
            if configInput == 8:
                currentMenu = 3
            # exit
            elif configInput == 9: 
                currentMenu = 0
                continue
            else:
                key = getConfigKeyFromInput(configInput)
                if key == 'removeUnusedStreets':
                    userInput = True 
                elif key == 'addUnusedStreets':
                    key = 'removeUnusedStreets'
                    userInput = False 
                else:
                    userInput = getNumberInput(0)
                currFlags[key] = userInput
                
        elif currentMenu == 3:
            algorithmInput = showAlgorithmMenu()

            # choose another file
            if algorithmInput == 6:
                currentMenu = 1
                continue
            # new configurations
            elif algorithmInput == 7:
                currentMenu = 2
            # go to main menu
            elif algorithmInput == 8:
                currentMenu = 0
                continue
            else:
                runAlgorithm(inputFile, outputFile, algorithmInput, flags)



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