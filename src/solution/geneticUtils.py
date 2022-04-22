import random

from solution.utils import copyIntersections
from model.Street import Street


def orderBasedCrossover(parent1, parent2):
    middlePoint = len(parent1)//2
    return parent1[:middlePoint] + parent2[middlePoint:]

def uniformCrossover(parent1Idx, parent2Idx, currPopulationFitness, currPopulation):
    parent1, parent2 = currPopulation[parent1Idx], currPopulation[parent2Idx]
    child = copyIntersections(parent1)

    p1Prob = currPopulationFitness[parent1Idx] / (currPopulationFitness[parent1Idx] + currPopulationFitness[parent2Idx])
    for intersectionIdx in range(len(parent1)):
        for streetIdx in range(len(parent1[intersectionIdx].incomingStreets)):
            if random.random() > p1Prob:
                child[intersectionIdx].updateSemaphoreAndCycleTime(streetIdx, parent2[intersectionIdx].incomingStreets[streetIdx][1])
    return child

def chooseParentsRandom(populationNum):
    return (random.randint(populationNum - 1), random.randint(populationNum - 1))

def chooseParentsRoulette(currPopulationFitness):
    sumFitness = sum(currPopulationFitness)

    randomProb = random.random()
    probCounter = currPopulationFitness[0] / sumFitness
    currElem = 0
    while True:
        probCounter += currPopulationFitness[currElem] / sumFitness
        if probCounter >= randomProb:
            break
        currElem += 1
    parent1Idx = currElem

    sumFitness -= currPopulationFitness[parent1Idx]

    randomProb = random.random()
    probCounter = currPopulationFitness[0 if parent1Idx != 0 else 1] / sumFitness
    currElem = 0
    while True:
        if currElem != parent1Idx:   # Skip child 1
            probCounter += currPopulationFitness[currElem] / sumFitness
            if probCounter >= randomProb:
                break
        currElem += 1

    parent2Idx = currElem
    return (parent1Idx, parent2Idx)

