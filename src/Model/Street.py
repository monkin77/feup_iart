class Street:
    def __init__(self, id, startIntersection, endIntersection, name, timeToCross):
        self.id = id
        self.startIntersection = startIntersection
        self.endIntersection = endIntersection
        self.name = name
        self.timeToCross = timeToCross
        self.waitingQueue = []

    def __str__(self):
        return "Street-" + str(self.id)

    def addCar(self, car):
        self.waitingQueue.append(car)