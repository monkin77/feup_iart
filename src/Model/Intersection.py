class Intersection:
    def __init__(self, id):
        self.id = id
        self.outgoingStreets = []
        self.incomingStreets = []
        self.semaphores = []
        self.cars = []

    def __str__(self):
        return "Intersection-" + str(self.id)

    def addIncomingStreet(self, street):
        self.incomingStreets.append(street)
        self.semaphores.append(0)

    def addOutgoingStreet(self, street):
        self.outgoingStreets.append(street)

    def changeSemaphore(self, id, time):
        self.semaphores[id] = time

    def changeAllSemaphores(self, time):
        for i in range(len(self.semaphores)):
            self.changeSemaphore(i, time)
