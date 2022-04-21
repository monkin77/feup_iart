from inputOutput import readInput, writeOutput
from Simulation import Simulation
from solution.Solution import Solution
from menus import *
from config import *


def runAlgorithm(algorithmInput):
    (intersections, cars, maxTime, bonusPoints) = readInput(
        INPUT_FOLDER + config['inputFile'])
    simulation = Simulation(cars, maxTime, bonusPoints)
    solution = Solution(intersections, simulation, config['maxTime'])

    if config['removeUnusedStreets']:
        solution.removeUnusedStreets()

    solution.setInitialSolution()

    if algorithmInput == 1:
        finalScore = solution.hillClimbingBasicRandom(config['maxIterations'])
    elif algorithmInput == 2:
        finalScore = solution.hillClimbingSteepest()
    elif algorithmInput == 3:
        if changeAnnealingConfig():  # Go back
            return

        finalScore = solution.simulatedAnnealing(
            config['initialTemperature'], config['alpha'], config['precision'], config['coolingSchedule']
        )
    elif algorithmInput == 4:
        if changeTabuConfig():
            return

        finalScore = solution.tabuSearch(
            config['maxIterations'], config['tabuNumCandidates'])
    elif algorithmInput == 5:
        if changeGeneticConfig():
            return

        finalScore = solution.generationalGenetic(
            config['populationSize'], config['maxIterations'], config['mutationProb'],
            config['useRoullete'], config['useUniformCrossover']
        )
    elif algorithmInput == 6:
        if changeGeneticConfig():
            return

        finalScore = solution.steadyGenetic(
            config['populationSize'], config['maxIterations'],
            config['mutationProb'], config['useRoullete'], config['useUniformCrossover']
        )

    if (config['showFinalSolution']):
        solution.show()

    print("Final score = ", finalScore)
    input("Press enter to go back...")
    writeOutput(OUTPUT_FOLDER + config['outputFile'] + ".txt", solution.intersections)


def program():
    currentMenu = 0

    while currentMenu != -1:
        clearScreen()

        if currentMenu == 0:  # main menu
            showMainMenu()
            currentMenu = 2

        elif currentMenu == 1:  # Choose input file
            fileOption = showFilesMenu()
            if fileOption == 7:
                currentMenu = 0
                continue
            else:
                currentMenu = 2

            config['inputFile'] = files[fileOption]
        elif currentMenu == 2:  # Choose general config
            choice = changeGeneralConfig()

            if choice == 7:  # choose algorithm
                currentMenu = 3

            elif choice == 8:  # exit
                currentMenu = 0
                continue

        elif currentMenu == 3:
            algorithmInput = showAlgorithmMenu()

            # choose another file
            if algorithmInput == 7:
                currentMenu = 1
                continue
            # new configurations
            elif algorithmInput == 8:
                currentMenu = 2
            # go to main menu
            elif algorithmInput == 9:
                currentMenu = 0
                continue
            else:
                runAlgorithm(algorithmInput)


if __name__ == "__main__":
    program()
# melhorar melhorar print inicial
