from model.Car import Car


class Simulation:
    def __init__(self, cars, maxTime, bonusPoints):
        self.cars = cars
        self.maxTime = maxTime
        self.bonusPoints = bonusPoints

    def eval(self, intersections):
        waitingQueues = {}  # Stores car Ids

        for intersection in intersections:
            for street in intersection.incomingStreets:
                waitingQueues[street[0].id] = [
                    car.id for car in street[0].waitingQueue
                ]
        cars = [Car(car.id, car.streets) for car in self.cars]

        points = 0
        for second in range(self.maxTime + 1):
            print("second", second)
            for intersection in intersections:
                if intersection.semaphoreCycleTime == 0:
                    currIterTime = 0
                else:
                    currIterTime = (second %
                                    intersection.semaphoreCycleTime) + 1
                timeCounter = 0

                greenSemaphoreIdx = -1
                for (idx, street) in enumerate(intersection.incomingStreets):
                    timeCounter += street[1]
                    if timeCounter >= currIterTime:
                        greenSemaphoreIdx = idx
                        break

                if greenSemaphoreIdx >= 0:
                    street = intersection.incomingStreets[greenSemaphoreIdx][0]
                    waitingQueue = waitingQueues[street.id]
                    if len(waitingQueue) > 0:
                        carId = waitingQueue.pop(0)
                        # print("Car", carId, "went through street", street.name, "at", second)
                        car = cars[carId]
                        if car.currStreet == len(car.streets) - 1:
                            points += self.bonusPoints + self.maxTime - second
                            car.remainingCrossingTime = -1  # Don't check this car anymore
                        else:
                            car.currStreet += 1
                            car.remainingCrossingTime = car.streets[car.currStreet].timeToCross

            for car in cars:
                if car.remainingCrossingTime > 0:
                    car.remainingCrossingTime -= 1

                    if car.remainingCrossingTime == 0:  # Add car to the next street
                        currStreet = car.streets[car.currStreet]
                        waitingQueues[currStreet.id].append(
                            car.id)     # Add car id to street's queue

        return points

    def eval2(self, intersections):
        waitingQueues = {}  # Stores car Ids
        intersectionsMap = {}

        for intersection in intersections:
            intersectionsMap[intersection.id] = intersection
            for street in intersection.incomingStreets:
                waitingQueues[street[0].id] = [
                    car.id for car in street[0].waitingQueue
                ]

        cars = [Car(car.id, car.streets) for car in self.cars]

        points = 0
        for second in range(self.maxTime):
            changedIntersections = {}
            for car in cars:
                # go through the street
                if car.remainingCrossingTime > 0:
                    car.remainingCrossingTime -= 1
                    if car.remainingCrossingTime == 0:
                        if car.currStreet == len(car.streets) - 1:
                            points += self.bonusPoints + self.maxTime - second - 1
                            car.remainingCrossingTime = -1  # Don't check this car anymore
                        else:
                            newCarStreet = car.streets[car.currStreet]
                            waitingQueues[newCarStreet.id].append(car.id)

                # Add car to the next street if he's at the end of street
                elif car.remainingCrossingTime == 0:
                    # get street and intersection where the car is
                    currStreet = car.streets[car.currStreet]
                    currIntersection = intersectionsMap[currStreet.endIntersection.id]

                    # already passed a car on this intersection semaphore
                    if currIntersection.id in changedIntersections:
                        continue

                    # get current time of the semaphore cycle
                    if currIntersection.semaphoreCycleTime == 0:
                        currIterTime = 0
                    else:
                        currIterTime = (second %
                                        currIntersection.semaphoreCycleTime) + 1

                    # get the idx of the street with green semaphore
                    timeCounter = 0
                    greenSemaphoreIdx = -1
                    for (idx, street) in enumerate(currIntersection.incomingStreets):
                        timeCounter += street[1]
                        if timeCounter >= currIterTime:
                            greenSemaphoreIdx = idx
                            break

                    if greenSemaphoreIdx >= 0:
                        # get queue of the street with green semaphore in the intersection
                        street = currIntersection.incomingStreets[greenSemaphoreIdx][0]
                        if street.id == currStreet.id:
                            waitingQueue = waitingQueues[street.id]

                            if len(waitingQueue) > 0:
                                carId = waitingQueue[0]
                                if car.id == carId:
                                    waitingQueue.pop(0)
                                    changedIntersections[currIntersection.id] = True
                                    print("Car", car.id, "went through street", currStreet.name, " at ", second)
                                    car.currStreet += 1
                                    car.remainingCrossingTime = car.streets[car.currStreet].timeToCross - 1

                                    if (car.remainingCrossingTime == 0):
                                        if car.currStreet == len(car.streets) - 1:
                                            points += self.bonusPoints + self.maxTime - second - 1
                                            car.remainingCrossingTime = -1  # Don't check this car anymore
                                        else:
                                            newCarStreet = car.streets[car.currStreet]
                                            waitingQueues[newCarStreet.id].append(car.id)

        return points
