from inputOutput import readInput

INPUT_FILE = "../input/a.txt"

if __name__ == "__main__":
    (intersections, cars, streets, totalTime, score) = readInput(INPUT_FILE)
    for inters in intersections:
        print(inters)
    for car in cars:
        print(car)
    for street in streets:
        print(street)
    print(totalTime, score)
