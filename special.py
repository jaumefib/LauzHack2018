infinity = float('inf')

import funcions

def hill_climbing(problem):
    """From the initial node, keep choosing the neighbor with highest value,
    stopping when no neighbor is better. [Figure 4.2]"""

    problem.cost = actualGraphCost(); # ToDo: David

    while True:
        lines = obtainLines() # ToDo: Oriol
        neighbours = obtainLinesMostUsed(lines) # ToDo: David

        b = True

        for i in neighbours:
            modifyFreq(negibour[i],"increment") # ToDo: David
            cost = calculateCost() # ToDo: David
            if problem.cost > cost:
                problem.cost = cost
                b = False
                break
        # If there is no better state we finish
        if b:
            break
        else:
            calculateGraph() # ToDo: David


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
    paintGraph() # ToDo: David


if __name__ == "__main__":
    main()
