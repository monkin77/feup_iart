from model.Intersection import Intersection

def copyIntersections(intersections):
        newIntersections = [
            Intersection(
                obj.id,
                [street for street in obj.outgoingStreets],
                [street for street in obj.incomingStreets],
                obj.semaphoreCycleTime,
                obj.simulationTime
            ) for obj in intersections
        ]

        return newIntersections
