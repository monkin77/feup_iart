class Solution:
    def __init__(self, intersections):
        self.intersections = intersections
    
    def setInitialSolution(self):
        for intersection in self.intersections:
            intersection.changeAllSemaphores(1)

    
