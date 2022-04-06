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
