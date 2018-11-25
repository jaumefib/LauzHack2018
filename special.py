infinity = float('inf')


def hill_climbing(problem):
    """From the initial node, keep choosing the neighbor with highest value,
    stopping when no neighbor is better. [Figure 4.2]"""

    problem.cost = actualGraphCost(); # ToDo: David

    while True:
        lines = obtainLines() # ToDo: Oriol
        neighbours = obtainLinesMostUsed(lines) # ToDo: David

        b = True

        for i in neighbours:
            cost = calculateCost(neighbours[i]) # ToDo: David
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

    def actions(self, state):
        """Returns the list of actions which are allowed to be taken from the given state"""
        # In this case increment or dicrease the frecuency
        allowed_actions = ["increment", "dicrease"]
        return allowed_actions

    def result(self, state, action):
        """Modify the state with the selected action"""
        modify(state,action) # ToDo: David


def main():
    print("Starting program")
    # Activate the database
    problem = NiceJourney(infinity)
    hill_climbing(problem)
    # print the resulting graph
    paintGraph() # ToDo: David


if __name__ == "__main__":
    main()
