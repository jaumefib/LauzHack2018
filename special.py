from funcions import *
from neo4j.v1 import GraphDatabase
import os

infinity = float('inf')

try:
    uri = "bolt://" + os.environ["DB_HOST"] + ":" + os.environ["DB_PORT"]
    driver = GraphDatabase.driver(uri, auth=(os.environ["DB_USER"], os.environ["DB_PASS"]))
except:
    print("[ERROR] DB connection failed.")
    exit(1)

def hill_climbing(problem):
    """From the initial node, keep choosing the neighbor with highest value,
    stopping when no neighbor is better. [Figure 4.2]"""
    lines = obtainLines()
    problem.cost = actualGraphCost(lines, 2*(24*60/5))
    print("Initial problem cost " + str(problem.cost))
    while True:
        lines = obtainLines()
        neighbours = obtainLinesMostUsed(lines)
        print("Lines in decreasing order of usage " + str(neighbours))

        b = True
        lineModified = 0
        print("Increase")
        for i in neighbours:
            c = modifyFreq(neighbours[i], "increase")
            print(str(neighbours[i]) + " " + str(c))
            if problem.cost > c:
                print("problem cost > cost")
                problem.cost = c
                print("New minimum cost " + str(problem.cost))
                b = False
                break
        if b:
            neighbours = obtainLinesLeastUsed(lines)
            print("Decrease")
            for i in neighbours:
                c = modifyFreq(neighbours[i], "decrease")
                print(str(neighbours[i]) + " " + str(c))
                if problem.cost > c:
                    print("problem cost > cost")
                    problem.cost = c
                    print("New minimum cost " + str(problem.cost))
                    b = False
                    break

        # If there is no better state we finish
        if b:
            break
        else:
            calculateGraph(lineModified)


class NiceJourney:
    """Problem of finding a better graph for the traveling options"""

    def __init__(self, value):
        self.cost = value


def problema():
    print("Starting program")
    # Activate the database
    problem = NiceJourney(infinity)
    hill_climbing(problem)
    # print the resulting graph
    paintGraph()

