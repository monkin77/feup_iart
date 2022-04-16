def getInput(minValue, maxValue):
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

def getNumberInput(minValue):
    userInput = input("Insert new value: ")
    while True:
        try:
            val = int(userInput)
            if val < minValue:
                userInput = input("Invalid new value, please insert a positive one: ")
            else:
                break
        except ValueError:
            userInput = input("Invalid new value, please insert a positive one: ")

    return val

def printMenu(options):
    print("\n***************************************")
    for key, value in options.items():
        print(str(key) + ". " + value)
    print("***************************************")

    return getInput(1, len(options))


def showMainMenu():
    options = {1: "Choose an input file", 2: "Exit"}
    inputOption = printMenu(options)
    if inputOption == 2:
        return -1
    return inputOption

def showFilesMenu():
    options = {1: 'a.txt', 2: 'b.txt', 3: 'c.txt', 4: 'd.txt', 5: 'e.txt', 6: 'f.txt', 7: 'Return to main menu'}
    return printMenu(options)

def getOption(options, input):
    return options[input]

def showAlgorithmMenu():
    options = {
        1: 'Hill Climbing Basic Random', 
        2: 'Hill Climbing Steepest Ascent', 
        3: 'Simulated Annealing', 
        4: 'Tabu Search', 
        5: 'Genetic', 
        6: 'Choose another file',
        7: 'Set New Configurations',
        8: 'Go to Main Menu',
    }
    return printMenu(options)


def getInitialConfig():
    options = {
        1: 'Remove Unused Streets       ------      (All)',
        2: 'Add Unused Streets          ------      (All)',
        3: 'Set Max Num Iterations      ------      (Hill Climbing Basic Random | Tabu Search)',
        4: 'Set Inicial Temperature     ------      (Simulated Annealing)',
        5: 'Set Alpha                   ------      (Simulated Annealing)',
        6: 'Set precision               ------      (Simulated Annealing)',
        7: 'Tabu Number of Candidates   ------      (Tabu Search)',
        8: 'Choose Algorithm',
        9: 'Go to Main Menu',
    }
    return printMenu(options)

def getConfigKeyFromInput(input):
    options = {
        1: 'removeUnusedStreets',
        2: 'addUnusedStreets',
        3: 'iterations',
        4: 'inicialTemperature',
        5: 'alpha',
        6: 'precision',
        7: 'tabuNumCandidates',
    }
    return options[input]