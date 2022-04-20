import math
import random

from solution.TabuSolution import TabuSolution
from Simulation import Simulation
import time

from solution.geneticUtils import *
from solution.utils import copyIntersections

class Solution:
    def __init__(self, intersections, simulation : Simulation, maxExecutionTime):
        self.intersections = intersections
        self.simulation = simulation
        self.maxExecutionTime = maxExecutionTime

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
        curSolution = copyIntersections(self.intersections)
        curScore = self.simulation.eval2(curSolution)
        iterationCounter = 0

        startTime = time.time()
        while iterationCounter < maxNumIterations and time.time() - startTime < self.maxExecutionTime:
            neighbourSolution = copyIntersections(curSolution)

            for intersection in neighbourSolution: # Random neighbour
                intersection.randomMutation()

            neighbourScore = self.simulation.eval2(neighbourSolution)
            if curScore < neighbourScore:
                curSolution = neighbourSolution
                curScore = neighbourScore
                iterationCounter = 0
            else:
                iterationCounter += 1
            # print("Basic Climb iteration with: ", curScore, " points")

        self.intersections = curSolution
        return curScore

    def hillClimbingSteepest(self):
        curSolution = copyIntersections(self.intersections)
        neighbourSolution = copyIntersections(curSolution)
        curScore = self.simulation.eval2(curSolution)

        startTime = time.time()
        while time.time() - startTime < self.maxExecutionTime:
            initialScore = curScore

            # Tries to find the best swap to the current iteration solution
            for intersectionIdx in range(len(iterationSolution)):
                iterIntersection = iterationSolution[intersectionIdx]
                for i in range(len(iterIntersection.incomingStreets) - 1):
                    for j in range(i + 1, len(iterIntersection.incomingStreets)):
                        neighbourSolution = copyIntersections(iterationSolution)
                        intersection = neighbourSolution[intersectionIdx]

                        intersection.swapLights(i, j)
                        neighbourScore = self.simulation.eval2(
                            neighbourSolution)
                        if (neighbourScore > curScore):
                            curScore = neighbourScore
                            curSolution = neighbourSolution

            # Maybe change only one position at random, for efficiency
            # Tries to find the best swap to the current iteration solution
            for intersectionIdx in range(len(iterationSolution)):
                iterIntersection = iterationSolution[intersectionIdx]
                for i in range(len(iterIntersection.incomingStreets)):
                    for j in range(len(iterIntersection.incomingStreets)):
                        if (i == j):
                            continue
                        neighbourSolution = copyIntersections(iterationSolution)
                        intersection = neighbourSolution[intersectionIdx]

                        intersection.switchLightPos(i, j)
                        neighbourScore = self.simulation.eval(
                            neighbourSolution)
                        if (neighbourScore > curScore):
                            curScore = neighbourScore
                            curSolution = neighbourSolution

            # Tries to find a better solution by changing semaphore's time and using them if they improve the solution
            neighbourSolution = copyIntersections(iterationSolution)
            for intersectionIdx in range(len(iterationSolution)):
                intersection = neighbourSolution[intersectionIdx]
                for i in range(len(intersection.incomingStreets)):
                    intersection.changeLightRandomTime(i)
                    neighbourScore = self.simulation.eval(neighbourSolution)
                    if (neighbourScore > curScore):
                        curScore = neighbourScore
                        curSolution = neighbourSolution
                        neighbourSolution = copyIntersections(curSolution)
                    else:
                        neighbourSolution = copyIntersections(iterationSolution)

            iterationSolution = curSolution
            if curScore == initialScore:
                break
            # print("\nSteepest Climb iteration with: ", curScore, " points")


        self.intersections = curSolution
        return curScore

    def simulatedAnnealing(self, t0, alpha, precision, coolingSchedule):
        curSolution = copyIntersections(self.intersections)
        curScore = self.simulation.eval(curSolution)
        iterationCounter = 0

        startTime = time.time()
        while time.time() - startTime < self.maxExecutionTime:
            temperature = coolingSchedule(t0, alpha, iterationCounter)
            if round(temperature, precision) == 0:
                break
            iterationCounter += 1

            neighbourSolution = copyIntersections(curSolution)

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

    def tabuSearch(self, maxIter, candidateListSize):
        # StartTenure = sqrt(N)
        tenure = startTenure = math.floor(math.sqrt(len(self.intersections)))

        bestSolution = copyIntersections(self.intersections)
        bestScore = self.simulation.eval2(bestSolution)
        candidateSolution = copyIntersections(bestSolution)
        candidateScore = bestScore

        tabuList = [TabuSolution(bestSolution, tenure)]
        iterationCounter = 0

        startTime = time.time()
        # max iterations since last improvement
        while iterationCounter <= maxIter and time.time() - startTime < self.maxExecutionTime:
            # print("score", bestScore, "iter", iterationCounter, "tenure", tenure)

            neighbourhood = self.getCandidates(candidateSolution, candidateListSize)
            for neighbour in neighbourhood:
                isTabu = False
                for tabu in tabuList:
                    if tabu.isSolutionTabu(neighbour):
                        # print("Tabu!")
                        isTabu = True
                        break
                if isTabu:
                    continue

                neighbourScore = self.simulation.eval2(neighbour)
                if neighbourScore > candidateScore:
                    candidateSolution = neighbour
                    candidateScore = neighbourScore

            if candidateScore > bestScore:
                bestSolution = candidateSolution
                bestScore = candidateScore
                iterationCounter = 0
                # No stagnation, return to startTenure
                tenure = startTenure
            else:
                iterationCounter += 1
                # Increase tenure when detecting stagnation
                tenure += 1

            # Update tabuList
            for tabu in tabuList:
                tabu.tenure -= 1
            tabuList = list(filter(lambda t: t.tenure > 0, tabuList))
            tabuList.append(TabuSolution(candidateSolution, tenure))

        self.intersections = bestSolution
        return bestScore

    # Add parameters for configuration
    def generationalGenetic(self, populationSize, maxIter, mutationProb, useRoullete, useUniformCrossover):
        currPopulation = self.getInitPopulation(populationSize)
        if useRoullete or useUniformCrossover:
            currPopulationFitness = [self.simulation.eval2(sol) for sol in currPopulation]

        startTime = time.time()
        currIter = 0
        while (time.time() - startTime < self.maxExecutionTime and currIter < maxIter):
            print("Curr Iter", currIter)
            newPopulation = []
            newPopulationFitness = []
            for _ in range(populationSize):
                if useRoullete:
                    (parent1Idx, parent2Idx) = chooseParentsRoullete(currPopulationFitness)
                else:
                    (parent1Idx, parent2Idx) = chooseParentsRandom(populationSize)

                if useUniformCrossover:
                    child = uniformCrossover(parent1Idx, parent2Idx, currPopulationFitness, currPopulation)
                else:
                    child = orderBasedCrossover(currPopulation[parent1Idx], currPopulation[parent2Idx])
                child = copyIntersections(child)

                if random.random() <= mutationProb:
                    randomIntersection = random.choice(child)
                    randomIntersection.randomMutation()
                
                newPopulation.append(child)
                if useRoullete or useUniformCrossover:
                    newPopulationFitness.append(self.simulation.eval2(child))

            currPopulation = newPopulation
            currPopulationFitness = newPopulationFitness
            
            currIter += 1
        
        if useRoullete or useUniformCrossover:
            bestSol = currPopulation[0]
            bestScore = currPopulationFitness[0]
            for idx in range(1, len(currPopulation)):
                if currPopulationFitness[idx] > bestScore:
                    bestScore = currPopulationFitness[idx]
                    bestSol = currPopulation[idx]
        else:
            bestSol = currPopulation[0]
            bestScore = self.simulation.eval2(bestSol)
            for solution in currPopulation[1:]:
                currScore = self.simulation.eval2(solution)
                if currScore > bestScore:
                    bestScore = currScore
                    bestSol = solution

        self.intersections = bestSol
        return bestScore

    def steadyGenetic(self, populationSize, maxIter, mutationProb, useRoullete, useUniformCrossover):
        currPopulation = self.getInitPopulation(populationSize)
        currPopulationFitness = [self.simulation.eval2(sol) for sol in currPopulation]

        startTime = time.time()
        currIter = 0
        while (time.time() - startTime < self.maxExecutionTime and currIter < maxIter):
            print("Curr Iter", currIter)
            if useRoullete:
                (parent1Idx, parent2Idx) = chooseParentsRoullete(currPopulationFitness)
            else:
                (parent1Idx, parent2Idx) = chooseParentsRandom(populationSize)

            if useUniformCrossover:
                child = uniformCrossover(parent1Idx, parent2Idx, currPopulationFitness, currPopulation)
            else:
                child = orderBasedCrossover(currPopulation[parent1Idx], currPopulation[parent2Idx])
            child = copyIntersections(child)

            if random.random() <= mutationProb:
                randomIntersection = random.choice(child)
                randomIntersection.randomMutation()
            
            childFitness = self.simulation.eval2(child)

            minVal = float('inf')
            minIdx = -1
            for i in range(len(currPopulationFitness)):
                if currPopulationFitness[i] < minVal:
                    minVal = currPopulationFitness[i]
                    minIdx = i
                
            currPopulationFitness[minIdx] = childFitness
            currPopulation[minIdx] = child
            
            currIter += 1
        
        bestSol = currPopulation[0]
        bestScore = currPopulationFitness[0]
        for idx in range(1, len(currPopulation)):
            if currPopulationFitness[idx] > bestScore:
                bestScore = currPopulationFitness[idx]
                bestSol = currPopulation[idx]

        self.intersections = bestSol
        return bestScore


    def getInitPopulation(self, populationSize):
        initPopulation = []
        initialSolution = copyIntersections(self.intersections)
        if len(initialSolution) != 0:
            initPopulation.append(initialSolution)
        
        clearIntersections = copyIntersections(self.intersections)
        for intersection in clearIntersections:
            intersection.changeAllSemaphores(0)

        while len(initPopulation) < populationSize:
            newCandidate = copyIntersections(clearIntersections)
            for intersection in newCandidate:
                for idx in range(len(intersection.incomingStreets)):
                    intersection.changeLightTime(idx, random.randint(0, self.simulation.maxTime / 2))

            initPopulation.append(newCandidate)

        return initPopulation

    def getCandidates(self, solution, candidateListSize):
        candidates = []
        for _ in range(candidateListSize):
            newCandidate = copyIntersections(solution)
            random.choice(newCandidate).randomMutation() # Random neighbour
            candidates.append(newCandidate)

        return candidates

    def show(self):
        for intersection in self.intersections:
            print("|| Intersection " + str(intersection.id) + " ||")
            semString = "["
            for (street, semaphore) in intersection.incomingStreets:
                semString += street.name + "-" + str(semaphore) + ", "
            semString = semString[:-2]  # remove last 2 characters
            semString += "]"
            print(semString)
