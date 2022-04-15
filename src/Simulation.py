from Model.Car import Car


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
