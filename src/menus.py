import os
from config import *

def getMenuChoice(minValue, maxValue):
    userInput = input("Insert option from the menu: ")
    while True:
        try:
            val = int(userInput)
            if val < minValue or val > maxValue:
                userInput = input("Invalid option, please insert a valid one: ")
            else:
                break
        except ValueError:
            userInput = input("Invalid option, please insert a valid one: ")

    return val

def printMenu(options, title):
    print("\n" + title, end="\n\n")
    print("********************************************************")
    for key, value in options.items():
        print(str(key) + ". " + value)
    print("********************************************************")

    return getMenuChoice(1, len(options))

def showMainMenu():
    print("\
#######                                          #####                                                \n\
   #    #####    ##   ###### ###### #  ####     #     # #  ####  #    #   ##   #      # #    #  ####  \n\
   #    #    #  #  #  #      #      # #    #    #       # #    # ##   #  #  #  #      # ##   # #    # \n\
   #    #    # #    # #####  #####  # #          #####  # #      # #  # #    # #      # # #  # #      \n\
   #    #####  ###### #      #      # #               # # #  ### #  # # ###### #      # #  # # #  ### \n\
   #    #   #  #    # #      #      # #    #    #     # # #    # #   ## #    # #      # #   ## #    # \n\
   #    #    # #    # #      #      #  ####      #####  #  ####  #    # #    # ###### # #    #  #### \n")

    print("Welcome to the Google Hashcode 2021 Solver, developed for the Artificial Intelligence course")
    input("Press enter to get started...\n")

def showFilesMenu():
    clearScreen()
    options = {
        1: 'An example (A)',
        2: 'By the ocean (B)',
        3: 'Checkmate (C)',
        4: 'Daily commute (D)',
        5: 'Etoile (E)',
        6: 'Forever jammed (F)',
        7: 'Custom Input 1',
        8: 'Custom Input 2',
    }
    inputOption = printMenu(options, "Choose Input File")
    config['inputFileLabel'] = options[inputOption]
    return inputOption

def getOption(options, input):
    return options[input]

def showAlgorithmMenu():
    options = {
        1: 'Hill Climbing Basic Random',
        2: 'Hill Climbing Steepest Ascent',
        3: 'Simulated Annealing',
        4: 'Tabu Search',
        5: 'Generational Genetic',
        6: 'Steady State Genetic',
        7: 'Set General Configurations',
        8: 'Go to Main Menu',
    }
    return printMenu(options, "Choose Algorithm")

def changeGeneralConfig():
    options = {
        1: f"Set Input File              ------   {config['inputFileLabel']}",
        2: f"Set Output File             ------   {config['outputFile']}",
        3: f"Set Max Num Iterations      ------   {config['maxIterations']}",
        4: f"Set Max Execution Time      ------   {config['maxTime']} secs",
        5: "Don't Show Final Solution"
        if config['showFinalSolution'] else
        "Show Final Solution",
        6: "Don't Remove Unused Streets"
        if config['removeUnusedStreets'] else
        "Remove Unused Streets",
        7: 'Choose Algorithm',
        8: 'Go to Main Menu',
    }

    configOption = printMenu(options, "General Configuration")
    if configOption >= len(options) - 1:
        return configOption

    if configOption == 1:
        fileOption = showFilesMenu()
        config['inputFile'] = files[fileOption]
    elif configOption == 2:
        changeOutputFile()
    elif configOption == 3:
        changeNumberConfig('maxIterations')
    elif configOption == 4:
        changeNumberConfig('maxTime')
    elif configOption == 5:
        changeBooleanConfig('showFinalSolution')
    elif configOption == 6:
        changeBooleanConfig('removeUnusedStreets')

    return configOption

def changeAnnealingConfig():
    while True:
        clearScreen()
        options = {
            1: f"Set Initial Temperature     ------   {config['initialTemperature']}",
            2: f"Set Cooling alpha Constant  ------   {config['alpha']}",
            3: f"Set Temperature Precision   ------   {config['precision']} decimal cases",
            4: f"Set Cooling Schedule        ------   {config['coolingSchedule'].__name__}",
            5: "Run Simulated Annealing",
            6: 'Choose Algorithm',
        }

        configOption = printMenu(options, "Configure Simulated Annealing")
        if configOption == len(options) - 1:
            return False  # Run Algorithm
        if configOption == len(options):
            return True  # Go back

        if configOption == 1:
            changeNumberConfig('initialTemperature')
        elif configOption == 2:
            changeNumberConfig('alpha', True)
        elif configOption == 3:
            changeNumberConfig('precision')
        elif configOption == 4:
            changeCoolingSchedule()

def changeCoolingSchedule():
    clearScreen()
    options = {
        1: "Exponential Cooling ( 0.8 <= alpha <= 0.9 ) \n T = T0 * (alpha ^ k)",
        2: "Logarithmical Cooling ( alpha > 1 ) \n T = T0 / (1 + alpha * ln(1 + k))",
        3: "Linear Cooling ( alpha > 0 ) \n T = T0 / (1 + alpha * k) ",
        4: "Quadratic Cooling ( alpha > 0 ) \n T = T0 / (1 + alpha * (k ^ 2)) ",
    }

    configOption = printMenu(options, "Choose Cooling Schedule")
    if configOption == 1:
        config['coolingSchedule'] = exponentialCooling
        config['alpha'] = 0.85
    elif configOption == 2:
        config['coolingSchedule'] = logarithmicalCooling
        config['alpha'] = 1.5
    elif configOption == 3:
        config['coolingSchedule'] = linearCooling
        config['alpha'] = 1
    elif configOption == 4:
        config['coolingSchedule'] = quadraticCooling
        config['alpha'] = 1

def changeTabuConfig():
    while True:
        clearScreen()
        options = {
            1: f"Set Number of Candidates  ------   {config['tabuNumCandidates']}",
            2: "Run Tabu Search",
            3: 'Choose Algorithm',
        }

        configOption = printMenu(options, "Configure Tabu Search")
        if configOption == len(options) - 1:
            return False  # Run Algorithm
        if configOption == len(options):
            return True  # Go back

        if configOption == 1:
            changeNumberConfig('tabuNumCandidates')

def changeGeneticConfig():
    while True:
        clearScreen()
        options = {
            1: f"Set Population Size      ------   {config['populationSize']}",
            2: f"Set Mutation Probability ------   {config['mutationProb']}",
            3: f"Use Random Selection     ------   Currently Using Roulette Selection"
                    if config['useRoulette'] else
                f"Use Roulette Selection   ------   Currently Using Random Selection",
            4: f"Use Order Base Crossover ------   Currently Using Uniform Crossover"
            if config['useUniformCrossover'] else
            f"Use Uniform Crossover    ------   Currently Using Order Base Crossover",
            5: "Run Genetic Algorithm",
            6: 'Choose Algorithm',
        }

        configOption = printMenu(options, "Configure Genetic Search")
        if configOption == len(options) - 1:
            return False  # Run Algorithm
        if configOption == len(options):
            return True  # Go back

        if configOption == 1:
            changeNumberConfig('populationSize')
        elif configOption == 2:
            changeNumberConfig('mutationProb', True, 1)
        elif configOption == 3:
            changeBooleanConfig('useRoulette')
        elif configOption == 4:
            changeBooleanConfig('useUniformCrossover')

def clearScreen():
    os.system('cls' if os.name == 'nt' else 'clear')
