class Solution:
    def __init__(self, intersections):
        self.intersections = intersections

    def setInitialSolution(self):
        for intersection in self.intersections:
            intersection.changeAllSemaphores(1)

    def removeUnusedStreets(self):
        for intersection in self.intersections:
            intersection.incomingStreets = [
                street for street in intersection.incomingStreets if street[0].carUsageCount != 0
            ]

    def show(self):
        for intersection in self.intersections:
            print("|| Intersection " + str(intersection.id) + " ||")
            semString = "["
            for (street, semaphore) in intersection.incomingStreets:
                semString += str(semaphore) + ", "
            semString = semString[:-2]  # remove last 2 characters
            semString += "]"
            print(semString)
