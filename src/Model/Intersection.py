import random

class Intersection:
    def __init__(self, id):
        self.id = id
        self.outgoingStreets = []
        self.incomingStreets = []
        self.cars = []

    def __str__(self):
        return "Intersection-" + str(self.id)

    def addIncomingStreet(self, street):
        self.incomingStreets.append((street, 0))

    def addOutgoingStreet(self, street):
        self.outgoingStreets.append(street)

    def changeSemaphore(self, id, time):
        self.incomingStreets[id][1] = time

    def changeAllSemaphores(self, time):
        for i in range(len(self.incomingStreets)):
            self.changeSemaphore(i, time)

    def swapLightsMutation(self):
        if len(self.incomingStreets <= 1):
            return

        idx1 = idx2 = random.randint(0, len(self.incomingStreets) - 1)
        while idx2 == idx1:
            idx2 = random.randint(0, len(self.incomingStreets) - 1)

        self.incomingStreets[idx1], self.incomingStreets[idx2] = self.incomingStreets[idx2], self.incomingStreets[idx1]

    def switchLightPosMutation(self):
        if len(self.incomingStreets <= 1):
            return
        
        idx1 = newIdx = random.randint(0, len(self.incomingStreets) - 1)
        while newIdx == idx1:
            newIdx = random.randint(0, len(self.incomingStreets) - 1)

        street = self.incomingStreets.pop(idx1)
        self.incomingStreets.insert(newIdx, street)

    def changeLightTimeMutation(self):
        idx = random.randint(0, len(self.incomingStreets) - 1)

        minTime = max(-10, 0 - self.incomingStreets[idx][1])
        time = random.choice([i for i in range(minTime, 11) if i != 0])
        self.incomingStreets[idx][1] += time
