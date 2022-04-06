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
        timeToCross = int(lines[i][3])


        newStreet = Street(
            i - 1,
            intersections[startIntersectionId],
            intersections[endIntersectionId],
            streetName,
            timeToCross
        )
        streets[streetName] = newStreet

        intersections[startIntersectionId].addOutgoingStreet(newStreet)
        intersections[endIntersectionId].addIncomingStreet(newStreet)

    for i in range(numStreets + 1, numStreets + numCars + 1):
        car = cars[i - numStreets - 1]
        numPathStreets = int(lines[i][0])
        for j in range(1, numPathStreets + 1):
            streetName = lines[i][j]
            car.streets.append(streets[streetName])
            streets[streetName].carUsageCount += 1
        firstStreetName = lines[i][1]
        streets[firstStreetName].addCar(car)

    return (intersections, cars, totalTime, score)


def writeOutput(fileName, intersections):
    f = open(fileName, "w")

    f.write(str(len(intersections)) + "\n")
    for intersection in intersections:
        f.write(str(intersection.id) + "\n")
        f.write(str(len(intersection.incomingStreets)) + "\n")

        for (idx, incStreet) in enumerate(intersection.incomingStreets):
            f.write(incStreet.name + " " + str(intersection.semaphores[idx]) + "\n")


    f.close()
