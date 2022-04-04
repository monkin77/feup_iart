class Intersection:
    def __init__(self, id):
        self.id = id
        self.outgoingStreets = []
        self.incomingStreets = []
        self.cars = []

    def __str__(self):
        return "Intersection-" + str(self.id)
