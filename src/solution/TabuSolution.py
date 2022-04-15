class TabuSolution:
    def __init__(self, intersections, tenure):
        self.intersections = intersections
        self.tenure = tenure

    def isSolutionTabu(self, intersections):
        if len(self.intersections) != len(intersections):
            return False

        for i in range(len(self.intersections)):
            intersection1 = self.intersections[i]
            intersection2 = intersections[i]

            # Different intersections or the same one with different incoming streets
            if intersection1.id != intersection2.id or len(intersection1.incomingStreets) != len(intersection2.incomingStreets):
                return False

            for j in range(len(intersection1.incomingStreets)):
                (street1, light1) = intersection1.incomingStreets[j]
                (street2, light2) = intersection2.incomingStreets[j]

                # Different streets or the same one with different green light times
                if street1.id != street2.id or light1 != light2:
                    return False

        return True
