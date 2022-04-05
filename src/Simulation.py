from functools import reduce

class Simulation:
    def __init__(self, intersections, cars, streets, maxTime, bonusPoints):
        self.intersections = intersections
        self.cars = cars
        self.streets = streets
        self.maxTime = maxTime
        self.bonusPoints = bonusPoints

    def eval(self):
        points = 0
        for second in range(self.maxTime):
            print("second:", second)

            for intersection in self.intersections:
                totalSemaphoreTime = reduce(lambda i1, i2: i1+i2, intersection.semaphores)  # Could be a property of Intersection
                if totalSemaphoreTime == 0:
                    currIterTime = 0
                else:
                    currIterTime = (second % totalSemaphoreTime) + 1
                timeCounter = 0

                greenSemaphoreIdx = -1
                for (idx, sem) in enumerate(intersection.semaphores):
                    timeCounter += sem
                    if timeCounter >= currIterTime:
                        greenSemaphoreIdx = idx
                        break
                print("totalSemTime:", totalSemaphoreTime, "currIterTime:", currIterTime)

                if greenSemaphoreIdx >= 0:
                    print("Green: ", intersection.incomingStreets[greenSemaphoreIdx].name)
                    street = intersection.incomingStreets[greenSemaphoreIdx]
                    if len(street.waitingQueue) > 0:
                        car = street.waitingQueue.pop(0)

                        if car.currStreet == len(car.streets) - 1:
                            points += self.bonusPoints + self.maxTime - 1 - second
                            car.remainingCrossingTime = -1  # Don't check this car anymore
                        else:
                            car.currStreet += 1
                            car.remainingCrossingTime = car.streets[car.currStreet].timeToCross

            for car in self.cars:
                if car.remainingCrossingTime > 0:
                    car.remainingCrossingTime -= 1

                    if car.remainingCrossingTime == 0:  # Add car to the next street
                        currStreet = car.streets[car.currStreet]
                        currStreet.addCar(car)  # Add car to street's queue

        return points

