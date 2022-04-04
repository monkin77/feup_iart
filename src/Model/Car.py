class Car:
    def __init__(self, id):
        self.id = id
        self.streets = []

    def __str__(self):
        return "Car-" + str(self.id)
