from Model.Intersection import Intersection
from Model.Car import Car
from Model.Street import Street

def readInput(fileName):
    lines = [line.strip().split(' ') for line in open(fileName, "r").readlines()]

    totalTime = int(lines[0][0])
    numIntersections = int(lines[0][1])
    numStreets = int(lines[0][2])
    numCars = int(lines[0][3])
    score = int(lines[0][4])

    intersections = [Intersection(id) for id in range(numIntersections)]
    cars = [Car(id) for id in range(numCars)]
    streets = {}

    for i in range(1, numStreets + 1):
        startIntersectionId = int(lines[i][0])
        endIntersectionId = int(lines[i][1])
        streetName = lines[i][2]
        timeToCross = lines[i][3]

        streets[streetName] = Street(
            i - 1,
            intersections[startIntersectionId],
            intersections[endIntersectionId],
            streetName,
            timeToCross
        )

    for i in range(numStreets + 1, numStreets + numCars + 1):
        numPathStreets = int(lines[i][0])
        for j in range(1, numPathStreets + 1):
            streetName = lines[i][j]
            cars[i - numStreets - 1].streets.append(streets[streetName])

    return (intersections, cars, streets.values(), totalTime, score)
