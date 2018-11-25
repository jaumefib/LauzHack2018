import random

def actualGraphCost():
    return random.randint(100, 120)


def obtainLines():
    return {1: "R1", 2: "R2", 3: "R3"}


def obtainLinesMostUsed(lines):
    return {2: "R2", 1: "R1", 3: "R3"}


def modifyFreq(linia, accio):
    if accio == "increment":
        r = 1
        # increment the frecuency of the line
        # only if the value is less than the maximum
    elif accio == "decrease":
        r = 2
        # decrease the frecuency of the line
        # only if the value is greater than the minimum


def calculateCost():
    return random.randint(40, 60)


def calculateGraph():
    calcular = 100
    # For the last modifyFreq with the modification in the line
    # change the graph 

def paintGraph():
    # paint the resultant graph
    print("Painting the graph")