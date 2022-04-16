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
        7: 'Go to Main Menu',
    }
    return printMenu(options)

