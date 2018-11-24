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

actStation = 0

def insertStation(ident, lon, lat, peopleIn, peopleOut):
    global actStation
    actStation = actStation + 1
    return actStation

def stationCleanIdent(ident):
    return ident.split(':')[0]

class Station:
    def __init__(self, ident, id, name, lat, lon, peopleIn, peopleOut):
        self.ident = ident
        self.id = id
        self.name = name
        self.lat = lat
        self.lom = lon
        self.peopleIn = peopleIn
        self.peopleOut = peopleOut

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
            # Create node
            stationId = insertStation(stationName, stationLat, stationLon, stationPeopleIn, stationPeopleOut)
            # Create station object with node id
            dataStations[stationIdent] = Station(stationIdent, stationId, stationName, stationLat, stationLon, stationPeopleIn, stationPeopleOut)

if __name__ == "__main__":
    main()