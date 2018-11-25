from funcions import *

infinity = float('inf')


def hill_climbing(problem):
    """From the initial node, keep choosing the neighbor with highest value,
    stopping when no neighbor is better. [Figure 4.2]"""

    problem.cost = actualGraphCost()
    print("Initial problem cost " + str(problem.cost))
    while True:
        lines = obtainLines()
        neighbours = obtainLinesMostUsed(lines)
        print("Lines in decreasing order of usage " + str(neighbours))

        b = True

        print("Increase")
        for i in neighbours:
            modifyFreq(neighbours[i], "increase")
            cost = calculateCost()
            print(str(neighbours[i]) + " " + str(cost))
            if problem.cost > cost:
                print("problem cost > cost")
                problem.cost = cost
                print("New minimum cost " + str(problem.cost))
                b = False
                break
        if b:
            neighbours = obtainLinesLeastUsed(lines)
            print("Decrease")
            for i in neighbours:
                modifyFreq(neighbours[i], "decrease")
                cost = calculateCost()
                print(str(neighbours[i]) + " " + str(cost))
                if problem.cost > cost:
                    print("problem cost > cost")
                    problem.cost = cost
                    print("New minimum cost " + str(problem.cost))
                    b = False
                    break

        # If there is no better state we finish
        if b:
            break
        else:
            calculateGraph()


class NiceJourney:
    """Problem of finding a better graph for the traveling options"""

    def __init__(self, value):
        self.cost = value


def main():
    print("Starting program")
    # Activate the database
    problem = NiceJourney(infinity)
    hill_climbing(problem)
    # print the resulting graph
    paintGraph()


if __name__ == "__main__":
    main()
