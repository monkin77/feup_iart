import random

def orderBased(parent1, parent2):
    middlePoint = len(parent1)//2
    return parent1[:middlePoint] + parent2[middlePoint:]

def chooseParentsRandom(currPopulation):
    return (random.choice(currPopulation), random.choice(currPopulation))

def chooseParentsRoullete(currPopulation, currPopulationFitness):
    sumFitness = sum(currPopulationFitness)

    probCounter = 0
    randomProb = random.random()
    currElem = 0
    while True:
        probCounter += currPopulationFitness[currElem] / sumFitness
        if probCounter >= randomProb:
            break
        currElem += 1
    child1Idx = currElem

    sumFitness -= currPopulationFitness[child1Idx]

    probCounter = 0
    randomProb = random.random()
    currElem = 0
    while True:
        if currElem != child1Idx:   # Skip child 1
            probCounter += currPopulationFitness[currElem] / sumFitness
            if probCounter >= randomProb:
                break
        currElem += 1

    child2Idx = currElem
    return (currPopulation[child1Idx], currPopulation[child2Idx])

