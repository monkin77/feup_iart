from inputOutput import readInput, writeOutput
from Simulation import Simulation

INPUT_FILE = "../input/a.txt"

if __name__ == "__main__":
    (intersections, cars, streets, maxTime, bonusPoints) = readInput(INPUT_FILE)

    '''
    for inters in intersections:
        print(inters)
    for car in cars:
        print(car)
    for street in streets:
        print(street)
    print(maxTime, bonusPoints)
    '''


    simulation = Simulation(intersections, cars, streets, maxTime, bonusPoints)
    result = simulation.eval()
    print("Total evaluation:", result)

    writeOutput('out.txt', intersections, cars, streets)

