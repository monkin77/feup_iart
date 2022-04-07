class Simulation:
    def __init__(self, intersections, cars, maxTime, bonusPoints):
        self.intersections = intersections
        self.cars = cars
        self.maxTime = maxTime
        self.bonusPoints = bonusPoints

    def eval(self):
        points = 0
        for second in range(self.maxTime):
            for intersection in self.intersections:
                if intersection.semaphoreCycleTime == 0:
                    currIterTime = 0
                else:
                    currIterTime = (second % intersection.semaphoreCycleTime) + 1
                timeCounter = 0

                greenSemaphoreIdx = -1
                for (idx, street) in enumerate(intersection.incomingStreets):
                    timeCounter += street[1]
                    if timeCounter >= currIterTime:
                        greenSemaphoreIdx = idx
                        break

                if greenSemaphoreIdx >= 0:
                    street = intersection.incomingStreets[greenSemaphoreIdx][0]
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

