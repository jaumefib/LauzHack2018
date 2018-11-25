import csv
import numpy as np

# Span (in seconds) for train frequencies
spanFrequencies = 15*60
# Span (in seconds) for passenger history
spanPeople = 15*60
# Span (in seconds) for data
spanData = 7*24*60*60
# Infrastructure data path
pathInfrastructure = "data/gtfs_complete/"
# Stations list
dataStations = {}
# Routes list
dataRoutes = {}
# Routes type list
dataRoutesTypes = {}
# Trips list
dataTrips = {}
# Services list
dataFrequencies = {}
# Unique lines list
dataUniqueLines = {}

actStation = 0

def insertStation(ident, lon, lat, peopleIn, peopleOut):
    global actStation
    actStation = actStation + 1
    return actStation

def stationCleanIdent(ident):
    return ident.split(':')[0]

def insertWalkable(idIn, idOut, kind, time):
    return True

def getLinkFreq(idIn, idOut, line, kind):
    return []

def insertLink(idIn, idOut, line, lineId, frequencies, people, kind, price):
    return True

def updateLink(idIn, idOut, line, lineId, frequencies, people, kind, price):
    return True

def tripCleanIdent(ident):
    return ident.split(':')[0]

def main():
    # Read stops
    with open(pathInfrastructure + 'stops.txt', 'r') as csvfile:
        csvReader = csv.reader(csvfile, delimiter=',')
        # Remove headers
        next(csvReader, None)
        # For each line on the CSV
        for csvLine in csvReader:
            stationIdent = stationCleanIdent(csvLine[0])
            stationName = csvLine[2]
            stationLat = float(csvLine[4])
            stationLon = float(csvLine[5])
            stationPeopleIn = [0] * int(spanData/spanPeople)
            stationPeopleOut = [0] * int(spanData/spanPeople)
            # Check if already exists
            if stationIdent not in dataStations:
                # Create node
                stationId = insertStation(stationName, stationLat, stationLon, stationPeopleIn, stationPeopleOut)
                # Create station object with node id
                dataStations[stationIdent] = stationId
    # Read transfers
    with open(pathInfrastructure + 'transfers.txt', 'r') as csvfile:
        csvReader = csv.reader(csvfile, delimiter=',')
        # Remove headers
        next(csvReader, None)
        # For each line on the CSV
        for csvLine in csvReader:
            walkableIdFrom = stationCleanIdent(csvLine[0])
            walkableIdTo = stationCleanIdent(csvLine[1])
            walkableKind = csvLine[2]
            walkableTime = csvLine[3]
            # Create edge
            insertWalkable(walkableIdFrom, walkableIdTo, walkableKind, walkableTime)
    # Read routes (lines)
    with open(pathInfrastructure + 'routes.txt', 'r') as csvfile:
        csvReader = csv.reader(csvfile, delimiter=',')
        # Remove headers
        next(csvReader, None)
        # For each line on the CSV
        for csvLine in csvReader:
            routeId = csvLine[0]
            routeName = csvLine[3]
            routeType = csvLine[5]
            dataRoutes[routeId] = routeName
            dataRoutesTypes[routeName] = routeType
    with open(pathInfrastructure + 'trips.txt', 'r') as csvfile:
        csvReader = csv.reader(csvfile, delimiter=',')
        # Remove headers
        next(csvReader, None)
        previousRoute = None
        # For each line on the CSV
        for csvLine in csvReader:
            tripRoute = csvLine[0]
            tripId = tripCleanIdent(csvLine[2])
            if tripRoute != previousRoute and tripId not in dataTrips:
                dataTrips[tripId] = tripRoute
                if tripId in dataFrequencies:
                    dataFrequencies[tripId] = dataFrequencies[tripId] + 1
                else:
                    dataFrequencies[tripId] = 1
            previousRoute = tripRoute
    with open(pathInfrastructure + 'stop_times.txt', 'r') as csvfile:
        csvReader = csv.reader(csvfile, delimiter=',')
        # Remove headers
        next(csvReader, None)
        previousTrip = ''
        previousStop = None
        # For each line on the CSV
        for csvLine in csvReader:
            stopTrip = csvLine[0]
            stopId = stationCleanIdent(csvLine[3])
            if tripCleanIdent(stopTrip) != tripCleanIdent(previousTrip):
                previousTrip = stopTrip
            elif stopTrip == previousTrip and tripCleanIdent(stopTrip) in dataTrips:
                linkIdIn = dataStations[previousStop]
                linkIdOut = stopId
                linkLineId = dataTrips[tripCleanIdent(stopTrip)]
                linkLine = dataRoutes[linkLineId]
                linkType = dataRoutesTypes[linkLine]
                linkFrequency = getLinkFreq(linkIdIn, linkIdOut, linkLine, linkType)
                linkFrequencyAct = [(float(dataFrequencies[tripCleanIdent(stopTrip)])/float(24*60/spanFrequencies))] * int(spanData/spanFrequencies)
                if linkFrequency == []:
                    insertLink(linkIdIn, linkIdOut, linkLineId, linkLine, linkFrequencyAct, [0] * int(spanData/spanPeople), linkType, 0)
                    dataUniqueLines[linkLineId] = linkLine
                else:
                    updateLink(linkIdIn, linkIdOut, linkLineId, linkLine, [x + y for x, y in zip(linkFrequency, linkFrequencyAct)], [0] * int(spanData / spanPeople), linkType, 0)
            previousStop = stopId
    for line in dataUniqueLines:
        print(line)

if __name__ == "__main__":
    main()