from copy import deepcopy
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

    def hillClimbingBasicRandom(self, maxNumIterations):
        curSolution = self.copyIntersections(self.intersections)
        curScore = self.simulation.eval(curSolution)
        iterationCounter = 0

        while iterationCounter < maxNumIterations:
            neighbourSolution = self.copyIntersections(curSolution)

            for intersection in neighbourSolution:
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
                obj.semaphoreCycleTime
            ) for obj in intersections
        ]

        return newIntersections
