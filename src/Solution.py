import math
import random

from Model.Intersection import Intersection

class Solution:
    def __init__(self, intersections, simulation):
        self.intersections = intersections
        self.simulation = simulation

    def setInitialSolution(self):
        for intersection in self.intersections:
            intersection.changeAllSemaphores(1)

    def removeUnusedStreets(self):
        for intersection in self.intersections:
            intersection.incomingStreets = [
                street for street in intersection.incomingStreets if street[0].carUsageCount != 0
            ]

        self.intersections = [
            intersection for intersection in self.intersections if len(intersection.incomingStreets) != 0
        ]

    def hillClimbingBasicRandom(self, maxNumIterations):
        curSolution = self.copyIntersections(self.intersections)
        curScore = self.simulation.eval(curSolution)
        iterationCounter = 0

        while iterationCounter < maxNumIterations:
            neighbourSolution = self.copyIntersections(curSolution)

            for intersection in neighbourSolution: # Random neighbour
                intersection.randomMutation()

            neighbourScore = self.simulation.eval(neighbourSolution)
            if curScore < neighbourScore:
                curSolution = neighbourSolution
                curScore = neighbourScore
                iterationCounter = 0
            else:
                iterationCounter += 1

        self.intersections = curSolution
        return curScore

    def hillClimbingSteepest(self):
        curSolution = self.copyIntersections(self.intersections)
        neighbourSolution = self.copyIntersections(curSolution)
        curScore = self.simulation.eval(curSolution)

        while True:
            initialScore = curScore

            for intersection in neighbourSolution:
                for i in range(len(intersection.incomingStreets) - 1):
                    for j in range(i + 1, len(intersection.incomingStreets)):
                        intersection.swapLights(i, j)
                        neighbourScore = self.simulation.eval(neighbourSolution)
                        if (neighbourScore > curScore):
                            curScore = neighbourScore
                            curSolution = neighbourSolution

                        neighbourSolution = self.copyIntersections(curSolution)

            # Maybe change only one position at random, for efficiency
            for intersection in neighbourSolution:
                for i in range(len(intersection.incomingStreets)):
                    for j in range(len(intersection.incomingStreets)):
                        if (i == j):
                            continue
                        intersection.switchLightPos(i, j)
                        neighbourScore = self.simulation.eval(neighbourSolution)
                        if (neighbourScore > curScore):
                            curScore = neighbourScore
                            curSolution = neighbourSolution

                        neighbourSolution = self.copyIntersections(curSolution)

            for intersection in neighbourSolution:
                for i in range(len(intersection.incomingStreets)):
                    intersection.changeLightRandomTime(i)
                    neighbourScore = self.simulation.eval(neighbourSolution)
                    if (neighbourScore > curScore):
                        curScore = neighbourScore
                        curSolution = neighbourSolution

                    neighbourSolution = self.copyIntersections(curSolution)

            if curScore == initialScore:
                break

        self.intersections = curSolution
        return curScore

    def simulatedAnnealing(self, t0, alpha, precision, coolingSchedule):
        curSolution = self.copyIntersections(self.intersections)
        curScore = self.simulation.eval(curSolution)
        iterationCounter = 0

        while True:
            temperature = coolingSchedule(t0, alpha, iterationCounter)
            if round(temperature, precision) == 0:
                break
            iterationCounter += 1

            neighbourSolution = self.copyIntersections(curSolution)

            random.choice(neighbourSolution).randomMutation() # Random neighbour
            neighbourScore = self.simulation.eval(neighbourSolution)

            diff = neighbourScore - curScore

            if diff > 0:
                curSolution = neighbourSolution
                curScore = neighbourScore
            else:
                probability = math.e ** (diff / temperature)
                if random.random() <= probability:
                    curSolution = neighbourSolution
                    curScore = neighbourScore

        self.intersections = curSolution
        return curScore

    def show(self):
        for intersection in self.intersections:
            print("|| Intersection " + str(intersection.id) + " ||")
            semString = "["
            for (_, semaphore) in intersection.incomingStreets:
                semString += str(semaphore) + ", "
            semString = semString[:-2]  # remove last 2 characters
            semString += "]"
            print(semString)

    def copyIntersections(self, intersections):
        newIntersections = [
            Intersection(
                obj.id,
                [street for street in obj.outgoingStreets],
                [street for street in obj.incomingStreets],
                obj.semaphoreCycleTime,
                obj.simulationTime
            ) for obj in intersections
        ]

        return newIntersections
