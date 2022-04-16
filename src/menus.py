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

def printMenu(options):
    print("\n***************************************")
    for key, value in options.items():
        print(str(key) + ". " + value)
    print("***************************************")

    return getMenuChoice(1, len(options))


def showMainMenu():
    options = {
        1: "Choose an input file",
        2: "Exit"
    }

    inputOption = printMenu(options)
    if inputOption == 2:
        return -1
    return inputOption

def showFilesMenu():
    options = {
        1: 'An example (A)',
        2: 'By the ocean (B)',
        3: 'Checkmate (C)',
        4: 'Daily commute (D)',
        5: 'Etoile (E)',
        6: 'Forever jammed (F)',
        7: 'Return to main menu'
    }
    return printMenu(options)

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
        7: 'Choose another file',
        8: 'Set General Configurations',
        9: 'Go to Main Menu',
    }
    return printMenu(options)


def changeGeneralConfig():
    options = {
        1: f"Set output file             ------   {config['outputFile']}",
        2: f"Set Max Num Iterations      ------   {config['maxIterations']}",
        3: f"Set Max Execution Time      ------   {config['maxTime']} secs",
        4: "Don't Remove Unused Streets"
                if config['removeUnusedStreets'] else
            "Remove Unused Streets",
        5: 'Choose Algorithm',
        6: 'Go to Main Menu',
    }

    configOption = printMenu(options)
    if configOption >= len(options) - 1:
        return configOption

    if configOption == 1:
        changeOutputFile()
    elif configOption == 2:
        changeNumberConfig('maxIterations')
    elif configOption == 3:
        changeNumberConfig('maxTime')
    elif configOption == 4:
        changeBooleanConfig('removeUnusedStreets')

    return configOption

def changeAnnealingConfig():
    clearScreen()
    while True:
        options = {
            1: f"Set Initial Temperature     ------   {config['initialTemperature']}",
            2: f"Set Cooling alpha Constant  ------   {config['alpha']}",
            3: f"Set Temperature Precision   ------   {config['precision']} decimal cases",
            4: f"Set Cooling Schedule        ------   {config['coolingSchedule'].__name__}",
            5: "Run Simulated Annealing",
            6: 'Choose Algorithm',
        }

        configOption = printMenu(options)
        if configOption == len(options) - 1:
            return False # Run Algorithm
        if configOption == len(options):
            return True # Go back

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

    configOption = printMenu(options)
    if configOption == 1:
        config['coolingSchedule'] = exponentialCooling
    elif configOption == 2:
        config['coolingSchedule'] = logarithmicalCooling
    elif configOption == 3:
        config['coolingSchedule'] = linearCooling
    elif configOption == 4:
        config['coolingSchedule'] = quadraticCooling

def changeTabuConfig():
    clearScreen()
    while True:
        options = {
            1: f"Set Number of Candidates  ------   {config['tabuNumCandidates']}",
            2: "Run Tabu Search",
            3: 'Choose Algorithm',
        }

        configOption = printMenu(options)
        if configOption == len(options) - 1:
            return False # Run Algorithm
        if configOption == len(options):
            return True # Go back

        if configOption == 1:
            changeNumberConfig('tabuNumCandidates')

def changeGeneticConfig():
    clearScreen()
    while True:
        options = {
            1: f"Set Population Size      ------   {config['populationSize']}",
            2: f"Set Mutation Probability ------   {config['mutationProb']}",
            3: f"Use Random Selection     ------   Now Using Roullete Selection"
                    if config['useRoullete'] else
                f"Use Roullete Selection   ------   Now Using Random Selection",
            4: f"Use Order Base Crossover ------   Now Using Uniform Crossover"
                    if config['useUniformCrossover'] else
                f"Use Uniform Crossover    ------   Now Using Order Base Crossover",
            5: "Run Genetic Algorithm",
            6: 'Choose Algorithm',
        }

        configOption = printMenu(options)
        if configOption == len(options) - 1:
            return False # Run Algorithm
        if configOption == len(options):
            return True # Go back

        if configOption == 1:
            changeNumberConfig('populationSize')
        elif configOption == 2:
            changeNumberConfig('mutationProb', True)
        elif configOption == 3:
            changeBooleanConfig('useRoullete')
        elif configOption == 4:
            changeBooleanConfig('useUniformCrossover')

def clearScreen():
    os.system('cls' if os.name == 'nt' else 'clear')
