import csv

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

actStation = 0

def insertStation(ident, lon, lat, peopleIn, peopleOut):
    global actStation
    actStation = actStation + 1
    return actStation

def stationCleanIdent(ident):
    return ident.split(':')[0]

def insertWalkable(idIn, idOut, kind, price):
    return True

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
            walkablePrice = csvLine[3]
            # Create edge
            insertWalkable(walkableIdFrom, walkableIdTo, walkableKind, walkablePrice)
    # Read routes (lines)
    with open(pathInfrastructure + 'routes.txt', 'r') as csvfile:
        csvReader = csv.reader(csvfile, delimiter=',')
        # Remove headers
        next(csvReader, None)
        # For each line on the CSV
        for csvLine in csvReader:
            routeId = csvLine[0]
            routeName = csvLine[3]
            dataRoutes[routeId] = routeName

if __name__ == "__main__":
    main()