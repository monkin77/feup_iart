import math
import random
import time

from config import *
from inputOutput import initCSV, saveResultCSV, printColoredText
from menus import clearScreen

from solution.TabuSolution import TabuSolution
from Simulation import Simulation

from solution.geneticUtils import *
from solution.utils import copyIntersections


class Solution:
    def __init__(self, intersections, simulation: Simulation, maxExecutionTime):
        self.intersections = intersections
        self.simulation = simulation
        self.maxExecutionTime = maxExecutionTime
        self.csv = initCSV(OUTPUT_FOLDER + config['outputFile'] + ".csv")

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
        curScore = self.simulation.eval(curSolution)
        stopCounter = 0
        iterationCounter = 0

        saveResultCSV(self.csv, 0, 0, curScore)

        startTime = time.time()
        while iterationCounter < maxNumIterations and time.time() - startTime < self.maxExecutionTime:
            print(
                f"Basic Climb iteration {iterationCounter} with: {curScore} points ({round(time.time()-startTime, 2)} seconds)", end="\r")
            neighbourSolution = copyIntersections(curSolution)

            for intersection in neighbourSolution:  # Random neighbour
                intersection.randomMutation()

            neighbourScore = self.simulation.eval(neighbourSolution)
            if curScore < neighbourScore:
                curSolution = neighbourSolution
                curScore = neighbourScore
                stopCounter = 0
            else:
                stopCounter += 1
            iterationCounter += 1
            saveResultCSV(self.csv, iterationCounter, time.time() - startTime, curScore)

        self.intersections = curSolution
        return curScore

    def hillClimbingSteepest(self):
        curSolution = copyIntersections(self.intersections)
        iterationSolution = copyIntersections(curSolution)
        curScore = self.simulation.eval(curSolution)

        iterationCounter = 0
        saveResultCSV(self.csv, 0, 0, curScore)

        startTime = time.time()
        while time.time() - startTime < self.maxExecutionTime:
            print(
                f"Steepest Climb iteration {iterationCounter} with: {curScore} points ({round(time.time()-startTime, 2)} seconds)", end="\r")

            initialScore = curScore

            # Tries to find the best swap to the current iteration solution
            for intersectionIdx in range(len(iterationSolution)):
                iterIntersection = iterationSolution[intersectionIdx]
                for i in range(len(iterIntersection.incomingStreets) - 1):
                    for j in range(i + 1, len(iterIntersection.incomingStreets)):
                        neighbourSolution = copyIntersections(
                            iterationSolution)
                        intersection = neighbourSolution[intersectionIdx]

                        intersection.swapLights(i, j)
                        neighbourScore = self.simulation.eval(
                            neighbourSolution)
                        if (neighbourScore > curScore):
                            curScore = neighbourScore
                            curSolution = neighbourSolution

            # Tries to find the best swap to the current iteration solution
            for intersectionIdx in range(len(iterationSolution)):
                iterIntersection = iterationSolution[intersectionIdx]
                for i in range(len(iterIntersection.incomingStreets)):
                    for j in range(len(iterIntersection.incomingStreets)):
                        if (i == j):
                            continue
                        neighbourSolution = copyIntersections(
                            iterationSolution)
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
                        neighbourSolution = copyIntersections(
                            iterationSolution)

            iterationSolution = curSolution
            if curScore == initialScore:
                break

            iterationCounter += 1
            saveResultCSV(self.csv, iterationCounter, time.time() - startTime, curScore)

        self.intersections = curSolution
        return curScore

    def simulatedAnnealing(self, t0, alpha, precision, coolingSchedule):
        curSolution = copyIntersections(self.intersections)
        curScore = self.simulation.eval(curSolution)
        iterationCounter = 0

        saveResultCSV(self.csv, 0, 0, curScore)

        startTime = time.time()
        while time.time() - startTime < self.maxExecutionTime:
            temperature = coolingSchedule(t0, alpha, iterationCounter)
            print(
                f"Simulated Annealing iteration {iterationCounter} at {round(temperature, precision)}?? with: {curScore} points ({round(time.time()-startTime, 2)} seconds)", end="\r")
            if round(temperature, precision) == 0:
                break
            iterationCounter += 1

            neighbourSolution = copyIntersections(curSolution)

            # Random neighbour
            random.choice(neighbourSolution).randomMutation()
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

            saveResultCSV(self.csv, iterationCounter, time.time() - startTime, curScore)

        self.intersections = curSolution
        return curScore

    def tabuSearch(self, maxIter, candidateListSize):
        # StartTenure = sqrt(N)
        tenure = startTenure = math.floor(math.sqrt(len(self.intersections)))

        bestSolution = copyIntersections(self.intersections)
        bestScore = self.simulation.eval(bestSolution)
        candidateSolution = copyIntersections(bestSolution)
        candidateScore = bestScore

        tabuList = [TabuSolution(bestSolution, tenure)]
        iterationCounter = 0
        generalCounter = 0
        saveResultCSV(self.csv, 0, 0, bestScore)

        startTime = time.time()
        # max iterations since last improvement
        while iterationCounter <= maxIter and time.time() - startTime < self.maxExecutionTime:
            print(
                f"Tabu Search iteration {generalCounter} with: {bestScore} points ({round(time.time()-startTime, 2)} seconds). Tenure = {tenure}", end="\r")
            neighbourhood = self.getCandidates(
                candidateSolution, candidateListSize)

            selectFirstNeighbour = True
            for neighbour in neighbourhood:
                isTabu = False
                for tabu in tabuList:
                    if tabu.isSolutionTabu(neighbour):
                        isTabu = True
                        break
                if isTabu:
                    continue

                neighbourScore = self.simulation.eval(neighbour)
                if selectFirstNeighbour or neighbourScore > candidateScore:
                    candidateSolution = neighbour
                    candidateScore = neighbourScore
                    selectFirstNeighbour = False

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

            generalCounter += 1
            saveResultCSV(self.csv, generalCounter, time.time() - startTime, bestScore)

        self.intersections = bestSolution
        return bestScore

    def generationalGenetic(self, populationSize, maxIter, mutationProb, useRoulette, useUniformCrossover):
        currPopulation = self.getInitPopulation(populationSize)
        currPopulationFitness = []
        bestScore = -1
        bestSolution = currPopulation[0]
        for sol in currPopulation:
            eval = self.simulation.eval(sol)
            currPopulationFitness.append(eval)
            if eval > bestScore:
                bestScore = eval
                bestSolution = sol
        saveResultCSV(self.csv, 0, 0, bestScore)

        startTime = time.time()
        currIter = 0
        while (time.time() - startTime < self.maxExecutionTime and currIter < maxIter):
            print(f"Generational GA iteration {currIter} with: {bestScore} points ({round(time.time()-startTime, 2)} seconds).", end="\r")
            newPopulation = []
            newPopulationFitness = []
            newBestScore = -1
            for _ in range(populationSize):
                if useRoulette:
                    (parent1Idx, parent2Idx) = chooseParentsRoulette(
                        currPopulationFitness)
                else:
                    (parent1Idx, parent2Idx) = chooseParentsRandom(populationSize)

                if useUniformCrossover:
                    child = uniformCrossover(
                        parent1Idx, parent2Idx, currPopulationFitness, currPopulation)
                else:
                    child = orderBasedCrossover(
                        currPopulation[parent1Idx], currPopulation[parent2Idx])
                child = copyIntersections(child)

                if random.random() <= mutationProb:
                    randomIntersection = random.choice(child)
                    randomIntersection.randomMutation()

                newPopulation.append(child)
                childFitness = self.simulation.eval(child)
                newPopulationFitness.append(childFitness)
                if childFitness > newBestScore:
                    newBestScore = childFitness
                    newBestSolution = child

            currPopulation = newPopulation
            currPopulationFitness = newPopulationFitness
            bestScore = newBestScore
            bestSolution = newBestSolution
            currIter += 1
            saveResultCSV(self.csv, currIter, time.time() - startTime, bestScore)

        self.intersections = bestSolution
        return bestScore

    def steadyGenetic(self, populationSize, maxIter, mutationProb, useRoulette, useUniformCrossover):
        currPopulation = self.getInitPopulation(populationSize)
        currPopulationFitness = []
        bestScore = -1
        for sol in currPopulation:
            eval = self.simulation.eval(sol)
            currPopulationFitness.append(eval)
            if eval > bestScore:
                bestScore = eval
        saveResultCSV(self.csv, 0, 0, bestScore)

        startTime = time.time()
        currIter = 0
        while (time.time() - startTime < self.maxExecutionTime and currIter < maxIter):
            print(f"Steady GA iteration {currIter} with: {bestScore} points ({round(time.time()-startTime, 2)} seconds).", end="\r")

            if useRoulette:
                (parent1Idx, parent2Idx) = chooseParentsRoulette(
                    currPopulationFitness)
            else:
                (parent1Idx, parent2Idx) = chooseParentsRandom(populationSize)

            if useUniformCrossover:
                child = uniformCrossover(
                    parent1Idx, parent2Idx, currPopulationFitness, currPopulation)
            else:
                child = orderBasedCrossover(
                    currPopulation[parent1Idx], currPopulation[parent2Idx])
            child = copyIntersections(child)

            if random.random() <= mutationProb:
                randomIntersection = random.choice(child)
                randomIntersection.randomMutation()
            
            childFitness = self.simulation.eval(child)
            if childFitness > bestScore:
                bestScore = childFitness
            currIter += 1
            saveResultCSV(self.csv, currIter, time.time() - startTime, bestScore)

            minVal = float('inf')
            minIdx = -1
            for i in range(len(currPopulationFitness)):
                if currPopulationFitness[i] < minVal:
                    minVal = currPopulationFitness[i]
                    minIdx = i

            currPopulationFitness[minIdx] = childFitness
            currPopulation[minIdx] = child
        
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
                    intersection.changeLightTime(idx, random.randint(0, int(math.sqrt(self.simulation.maxTime)) ) )

            initPopulation.append(newCandidate)

        return initPopulation

    def getCandidates(self, solution, candidateListSize):
        candidates = []
        for _ in range(candidateListSize):
            newCandidate = copyIntersections(solution)
            random.choice(newCandidate).randomMutation()  # Random neighbour
            candidates.append(newCandidate)

        return candidates

    def show(self):
        clearScreen()
        for intersection in self.intersections:
            printColoredText("| Intersection " + str(intersection.id) + " |")
            semString = "["
            for (street, semaphore) in intersection.incomingStreets:
                semString += street.name + " (" + str(semaphore) + "), "
            semString = semString[:-2]  # remove last 2 characters
            semString += "]"
            print(semString)

    def close(self):
        self.csv.close()
