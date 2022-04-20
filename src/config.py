from solution.coolingSchedule import *
from math import inf

INPUT_FOLDER = "input/"
OUTPUT_FOLDER = "output/"

files = {
    1: 'a.txt',
    2: 'b.txt',
    3: 'c.txt',
    4: 'd.txt',
    5: 'e.txt',
    6: 'f.txt',
}

config = {
    # I/O
    'inputFile': 'a.txt',
    'inputFileLabel': 'An example (A)',
    'outputFile': 'out',

    # General
    'removeUnusedStreets': False,
    'maxIterations': float('inf'),
    'maxTime': 60 * 2,

    # Simmulated Annealing
    'initialTemperature': 100,
    'alpha': 0.85,
    'precision': 10,
    'coolingSchedule': exponentialCooling,

    # Tabu Search
    'tabuNumCandidates': 10,

    # Genetic
    'populationSize': 8,
    'mutationProb': 0.05,
    'useRoullete': True,
    'useUniformCrossover': True,
}

def changeBooleanConfig(key):
    config[key] = not config[key]

def changeNumberConfig(key, isFloat = False, maxValue=inf):
    newNumber = getNumberInput(0, isFloat, maxValue)
    config[key] = newNumber

def changeOutputFile():
    userInput = input("Insert the output file's name: ")
    config['outputFile'] = userInput

def getNumberInput(minValue,  isFloat, maxValue = inf):
    userInput = input("Insert new value: ")
    while True:
        try:
            val = float(userInput) if isFloat else int(userInput)
            if val < minValue:
                userInput = input("Invalid new value, please insert a number above " + str(minValue) + ": ")
            elif val > maxValue:
                userInput = input("Invalid new value, please insert a number below " + str(maxValue) + ": ")
            else:
                break
        except ValueError:
            userInput = input("Invalid new value, please insert a valid number: ")

    return val
