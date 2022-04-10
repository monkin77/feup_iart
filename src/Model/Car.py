class Car:
    def __init__(self, id, streets):
        self.id = id
        self.streets = streets
        self.currStreet = 0
        self.remainingCrossingTime = 0

    def __str__(self):
        return "Car-" + str(self.id)
