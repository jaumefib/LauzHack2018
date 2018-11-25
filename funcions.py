import random
import operator

quantityInLine, typeOfTransport, frecuencyOfLine = []
cost = 0

def actualGraphCost():
    global quantityInLine, typeOfTransport, frecuencyOfLine
    quantityInLine = session.read_transaction(getLinkFreq, linkIdIn, linkIdOutGraph, linkLine, linkType)
    typeOfTransport = session.read_transaction()
    frecuencyOfLine = session.read_transaction()
    global cost
    cost = 0
    keys = quantityInLine.keys()
    for i in quantityInLine:
        users = quantityInLine[i]
        type = typeOfTransport[keys[i]]
        frec = frecuencyOfLine[keys[i]]
        capacity = 0
        if type == 0:
            capacity = 90
        elif type == 1:
            capacity = 100
        elif type == 2:
            capacity = 270
        elif type == 3:
            capacity = 90
        elif type == 4:
            capacity = 500
        elif type == 5:
            capacity = 6
        else:
            capacity = 5
        cost = cost + (users - capacity*frec)**2
    return cost


def obtainLines():
    global quantityInLine
    return quantityInLine.values()

def obtainLinesMostUsed(lines):
    #quantityInLine = session.read_transaction(getLinkFreq, linkIdIn, linkIdOutGraph, linkLine, linkType)
    #return sorted(quantityInLine.items(),key=operator.itemgetter(1))
    global quantityInLine
    return sorted(quantityInLine.values())


def obtainLinesLeastUsed(lines):
    #quantityInLine = session.read_transaction(getLinkFreq, linkIdIn, linkIdOutGraph, linkLine, linkType)
    #return sorted(quantityInLine.items(), key=operator.itemgetter(1))
    global quantityInLine
    return sorted(quantityInLine, key=quantityInLine.get, reverse = True)


def modifyFreq(linia, accio):
    global quantityInLine, typeOfTransport, frecuencyOfLine, cost
    user = quantityInLine[linia]
    freq = frecuencyOfLine[linia]
    type = typeOfTransport[linia]
    if type == 0:
        capacity = 90
    elif type == 1:
        capacity = 100
    elif type == 2:
        capacity = 270
    elif type == 3:
        capacity = 90
    elif type == 4:
        capacity = 500
    elif type == 5:
        capacity = 6
    else:
        capacity = 5
    if accio == "increment":
        # increment the frecuency of the line
        # only if the value is less than the maximum
        if freq+2 < 15:
            cost = cost - (user - capacity*freq)**2 + (user - capacity*(freq+2))**2
            frecuencyOfLine[linia] = freq+2
    elif accio == "decrease":
        # decrease the frecuency of the line
        # only if the value is greater than the minimum
        if freq-2 >= 0:
            cost = cost - (user - capacity * freq) ** 2 + (user - capacity * (freq - 2)) ** 2
            frecuencyOfLine[linia] = freq-2
    return cost

def calculateGraph(linia):
    # For the last modifyFreq with the modification in the line
    # change the graph


def paintGraph():
    # paint the resultant graph
    print("Painting the graph")