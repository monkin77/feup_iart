import random
from functools import reduce

class Intersection:
    def __init__(self, id, outgoingStreets, incomingStreets, semaphoreCycleTime, simulationTime):
        self.id = id
        self.outgoingStreets = outgoingStreets
        self.incomingStreets = incomingStreets
        self.semaphoreCycleTime = semaphoreCycleTime
        self.simulationTime = simulationTime

        self.mutationFunctions = [
            self.swapLightsMutation,
            self.switchLightPosMutation,
            self.changeLightTimeMutation
        ]

    def __str__(self):
        return "Intersection-" + str(self.id)

    def addIncomingStreet(self, street):
        self.incomingStreets.append((street, 0))

    def addOutgoingStreet(self, street):
        self.outgoingStreets.append(street)

    def updateSemaphoreAndCycleTime(self, incStreetIdx, newTime):
        oldStreet = self.incomingStreets[incStreetIdx]
        self.semaphoreCycleTime += newTime - oldStreet[1]
        self.incomingStreets[incStreetIdx] = (oldStreet[0], newTime)

    # Doesn't update semaphoreCycleTime
    def _changeSemaphore(self, id, time):
        oldStreet = self.incomingStreets[id]
        self.incomingStreets[id] = (oldStreet[0], time)

    def changeAllSemaphores(self, time):
        for i in range(len(self.incomingStreets)):
            self._changeSemaphore(i, time)
        self.semaphoreCycleTime = reduce(lambda acc, i2: acc + i2[1], self.incomingStreets, 0)

    def swapLights(self, idx1, idx2):
        self.incomingStreets[idx1], self.incomingStreets[idx2] = self.incomingStreets[idx2], self.incomingStreets[idx1]

    def swapLightsMutation(self):
        if len(self.incomingStreets) <= 1:
            return

        idx1 = random.randint(0, len(self.incomingStreets) - 1)
        idx2 = random.choice([i for i in range(0, len(self.incomingStreets)) if i != idx1])

        self.swapLights(idx1, idx2)

    def switchLightPos(self, idx, newIdx):
        street = self.incomingStreets.pop(idx)
        self.incomingStreets.insert(newIdx, street)

    def switchLightPosMutation(self):
        if len(self.incomingStreets) <= 1:
            return
        
        idx = newIdx = random.randint(0, len(self.incomingStreets) - 1)
        newIdx = random.choice([i for i in range(0, len(self.incomingStreets)) if i != idx])

        self.switchLightPos(idx, newIdx)

    def changeLightTime(self, idx, time):
        oldStreet = self.incomingStreets[idx]
        self.incomingStreets[idx] = (oldStreet[0], oldStreet[1] + time)
        self.semaphoreCycleTime += time

    def changeLightRandomTime(self, idx):
        minTime = max(-10, 0 - self.incomingStreets[idx][1])
        maxTime = min(10, self.simulationTime - self.incomingStreets[idx][1])
        time = random.choice([i for i in range(minTime, maxTime + 1) if i != 0])
        self.changeLightTime(idx, time)

    def changeLightTimeMutation(self):
        idx = random.randint(0, len(self.incomingStreets) - 1)
        self.changeLightRandomTime(idx)

    def randomMutation(self):
        idx = random.randint(0, len(self.mutationFunctions) - 1)
        self.mutationFunctions[idx]()
