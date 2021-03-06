import csv
from neo4j.v1 import GraphDatabase
import os
import time
from datetime import datetime
import ijson
#from special import *

# Span (in seconds) for train frequencies
spanFrequencies = 15*60
# Span (in seconds) for passenger history
spanPeople = 15*60
# Span (in seconds) for data
spanData = 7*24*60*60
# Infrastructure data path
pathInfrastructure = "gtfs_complete/"
# FairTIQ data path
pathPeople = "data/"
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
# Stations set
onlyStations = {}
# Routes set
onlyRoutes = {}
# Routes types
onlyTypes = {}

actStation = 0


def insertStation(tx, station, long, lat, peopleIn, peopleOut):
    for record in tx.run("CREATE (s:STATION) "
                         "SET s.station = {station}, "
                         "s.long = {long}, "
                         "s.lat = {lat}, "
                         "s.peopleIn = {peopleIn}, "
                         "s.peopleOut = {peopleOut} "
                         "RETURN id(s)", station=station, long=long, lat=lat, peopleIn=peopleIn, peopleOut=peopleOut):
        return record["id(s)"]


def stationCleanIdent(ident):
    return ident.split(':')[0]


def insertWalkable(tx, idIn, idOut, kind, time):
    for record in tx.run("MATCH (s1:STATION), (s2:STATION) "
                         "WHERE id(s1) = {idIn} AND id(s2) = {idOut} "
                         "CREATE (s1)-[:TRANSBORD { kind: {kind}, time: {time}}]->(s2)",
                         idIn=idIn, idOut=idOut, kind=kind, time=time):
        return True


def getLinkFreq(tx, idIn, idOut, line, kind):
    for record in tx.run("MATCH (s1:STATION), (s2:STATION) "
                         "WHERE id(s1) = {idIn} AND id(s2) = {idOut} "
                         "MATCH (s1)-[R:LINE {line: {line}, kind: {kind}}]->(s2) "
                         "RETURN R.frequencies",
                         idIn=idIn, idOut=idOut, line=line, kind=kind):
        return record["R.frequencies"]


def getLinkPeople(tx, idIn, idOut, line, kind):
    for record in tx.run("MATCH (s1:STATION), (s2:STATION) "
                         "WHERE id(s1) = {idIn} AND id(s2) = {idOut} "
                         "MATCH (s1)-[R:LINE {line: {line}, kind: {kind}}]->(s2) "
                         "RETURN R.people",
                         idIn=idIn, idOut=idOut, line=line, kind=kind):
        return record["R.people"]


def insertLink(tx, idIn, idOut, line, lineId, frequencies, people, kind, price):
    for record in tx.run("MATCH (s1:STATION), (s2:STATION) "
                         "WHERE id(s1) = {idIn} AND id(s2) = {idOut} "
                         "CREATE (s1)-[:LINE { lineId: {lineId}, line: {line}, frequencies: {frequencies}, people: {people}, kind: {kind}, price: {price}}]->(s2) ",
                         idIn=idIn, idOut=idOut, lineId=lineId, line=line, frequencies=frequencies, people=people, kind=kind,
                         price=price):
        return True


def updateLink(tx, idIn, idOut, line, frequencies, kind):
    for record in tx.run("MATCH (s1:STATION), (s2:STATION) "
                         "WHERE id(s1) = {idIn} AND id(s2) = {idOut} "
                         "MATCH (s1)-[R:LINE { line: {line}, kind: {kind}}]->(s2) SET R.frequencies = {frequencies}",
                         idIn=idIn, idOut=idOut, line=line, frequencies=frequencies, kind=kind):
        return True


def updateLinkPeople(tx, idIn, idOut, line, people, kind):
    for record in tx.run("MATCH (s1:STATION), (s2:STATION) "
                         "WHERE id(s1) = {idIn} AND id(s2) = {idOut} "
                         "MATCH (s1)-[R:LINE { line: {line}, kind: {kind}}]->(s2) SET R.frequencies = {people}",
                         idIn=idIn, idOut=idOut, line=line, people=people, kind=kind):
        return True


def tripCleanIdent(ident):
    return ident.split(':')[0]


def main():
    try:
        uri = "bolt://" + os.environ["DB_HOST"] + ":" + os.environ["DB_PORT"]
        driver = GraphDatabase.driver(uri, auth=(os.environ["DB_USER"], os.environ["DB_PASS"]))
    except:
        print("[ERROR] DB connection failed.")
        exit(1)
    with driver.session() as session:
        # Read stations
        with open(pathPeople + 'fairtiq_dataset.json', 'r') as jsonFile:
            for segment in ijson.items(jsonFile, 'item.segments.item'):
                segmentStationFrom = segment["startStation"]["id"]
                segmentStationTo = segment["endStation"]["id"]
                onlyStations[segmentStationFrom] = segment["startStation"]["name"]
                onlyStations[segmentStationTo] = segment["endStation"]["name"]
                if "route" in segment:
                    actName = segment["route"]["name"]
                    if segment["route"]["name"] not in onlyRoutes:
                        onlyRoutes[actName] = [(segmentStationFrom, segmentStationTo)]
                        onlyTypes[actName] = int(segment["route"]["type"])
                    else:
                        onlyRoutes[actName].append((segmentStationFrom, segmentStationTo))
        print("FINISH")
        for station in onlyStations:
            stationName = onlyStations[station]
            stationLat = 0.0
            stationLon = 0.0
            stationPeopleIn = [0] * int(spanData / spanPeople)
            stationPeopleOut = [0] * int(spanData / spanPeople)
            stationId = session.read_transaction(insertStation, stationName, stationLat, stationLon,
                                                         stationPeopleIn, stationPeopleOut)
            dataStations[station] = stationId
        for routeName, routeData in onlyRoutes.items():
            for routeDataAct in routeData:
                linkIdIn = dataStations[routeDataAct[0]]
                linkIdOut = dataStations[routeDataAct[1]]
                linkLineId = routeName
                linkLine = routeName
                linkType = onlyTypes[routeName]
                linkFrequency = session.read_transaction(getLinkFreq, linkIdIn, linkIdOut, linkLine, linkType)
                linkFrequencyAct = [1] * int(spanData / spanFrequencies)
                if linkFrequency == None:
                    session.read_transaction(insertLink, linkIdIn, linkIdOut, linkLine, linkLineId,
                                             linkFrequencyAct, [0] * int(spanData / spanPeople), linkType, 0)
                    dataUniqueLines[linkLineId] = linkLine
                else:
                    session.read_transaction(updateLink, linkIdIn, linkIdOut, linkLine,
                                             [x + y for x, y in zip(linkFrequency, linkFrequencyAct)], linkType)

        '''# Read stops
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
                if stationIdent not in dataStations and stationIdent in onlyStations:
                    # Create node
                    stationId = session.read_transaction(insertStation, stationName, stationLat, stationLon, stationPeopleIn, stationPeopleOut)
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
                session.read_transaction(insertWalkable, dataStations[walkableIdFrom], dataStations[walkableIdTo], walkableKind, walkableTime)
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
                if stopId in onlyStations:
                    if tripCleanIdent(stopTrip) != tripCleanIdent(previousTrip):
                        previousTrip = stopTrip
                    elif stopTrip == previousTrip and tripCleanIdent(stopTrip) in dataTrips:
                        linkIdIn = dataStations[previousStop]
                        linkIdOut = stopId
                        linkIdOutGraph = dataStations[linkIdOut]
                        linkLineId = dataTrips[tripCleanIdent(stopTrip)]
                        linkLine = dataRoutes[linkLineId]
                        linkType = dataRoutesTypes[linkLine]
                        linkFrequency = session.read_transaction(getLinkFreq, linkIdIn, linkIdOutGraph, linkLine, linkType)
                        linkFrequencyAct = [(float(dataFrequencies[tripCleanIdent(stopTrip)])/float(24*60/spanFrequencies))] * int(spanData/spanFrequencies)
                        if linkFrequency == None:
                            session.read_transaction(insertLink, linkIdIn, linkIdOutGraph, linkLine, linkLineId, linkFrequencyAct, [0] * int(spanData/spanPeople), linkType, 0)
                            dataUniqueLines[linkLineId] = linkLine
                        else:
                            session.read_transaction(updateLink, linkIdIn, linkIdOutGraph, linkLine, [x + y for x, y in zip(linkFrequency, linkFrequencyAct)], linkType)
                    previousStop = stopId'''
        '''with open(pathInfrastructure + 'frequencies.txt', 'r') as csvfile:
            csvReader = csv.reader(csvfile, delimiter=',')
            # Remove headers
            next(csvReader, None)
            previousTrip = ''
            previousStop = None
            # For each line on the CSV
            for csvLine in csvReader:
                freqTrip = csvLine[0]
                freqStart = csvLine[1]
                freqTo = csvLine[2]
                freqTime = csvLine[3]
                freqStartTime = time.strptime(freqStart, "%H:%M:%S")
                freqToTime = time.strptime(freqTo, "%H:%M:%S")
                freqElapsed = freqToTime - freqStartTime
                freqElapsedTimes = int(freqElapsed.total_seconds()/spanFrequencies)
                freqElapsedTimesFrom = int((freqStartTime - time.strptime("00:00:00", "%H:%M:%S")).total_seconds()/spanFrequencies)
                freqIni = [0] * int(spanData/spanFrequencies)
                for i in range(0, freqElapsedTimes):
                    freqIni[freqElapsedTimesFrom + i] = freqTime/spanFrequencies


                if tripCleanIdent(stopTrip) != tripCleanIdent(previousTrip):
                    previousTrip = stopTrip
                elif stopTrip == previousTrip and tripCleanIdent(stopTrip) in dataTrips:
                    linkIdIn = dataStations[previousStop]
                    linkIdOut = stopId
                    linkLineId = dataTrips[tripCleanIdent(stopTrip)]
                    linkLine = dataRoutes[linkLineId]
                    linkType = dataRoutesTypes[linkLine]
                    linkFrequency = session.read_transaction(getLinkFreq, linkIdIn, linkIdOut, linkLine, linkType)
                    linkFrequencyAct = [(float(dataFrequencies[tripCleanIdent(stopTrip)])/float(24*60/spanFrequencies))] * int(spanData/spanFrequencies)
                    if linkFrequency == []:
                        session.read_transaction(upsertLink, linkIdIn, linkIdOut, linkLineId, linkLine, linkFrequencyAct, [0] * int(spanData/spanPeople), linkType, 0)
                        dataUniqueLines[linkLineId] = linkLine
                    else:
                        session.read_transaction(upsertLink, linkIdIn, linkIdOut, linkLineId, linkLine, [x + y for x, y in zip(linkFrequency, linkFrequencyAct)], [0] * int(spanData / spanPeople), linkType, 0)
                previousStop = stopId'''
        '''with open(pathPeople + 'fairtiq_dataset.json', 'r') as jsonFile:
            for segment in ijson.items(jsonFile, 'item.segments.item'):
                print(segment)
                segmentStationFrom = segment["startStation"]["id"]
                segmentStationTo = segment["endStation"]["id"]
                segmentTimeFrom = datetime.strptime(segment["startAt"], "%Y-%m-%dT%H:%M:%S.%fZ")
                segmentTimeTo = datetime.strptime(segment["endAt"], "%Y-%m-%dT%H:%M:%S.%fZ")
                segmentDuration = int((segmentTimeTo - segmentTimeFrom).total_seconds()/spanPeople)
                segmentDay = segmentTimeFrom.weekday()
                segmentIni = int((segmentTimeFrom - datetime.strptime(str(segmentTimeFrom.year) + "-" + str(segmentTimeFrom.month) + "-" + str(segmentTimeFrom.day) + "T00:00:00", "%Y-%m-%dT%H:%M:%S")).total_seconds()/spanPeople)
                segmentKind = int(segment["route"]["type"])
                for i in range(0, segmentDuration):
                    freqPos = (int((segmentDay*24*60)/spanPeople)+segmentIni+i)
                    # Cridar funció get i update'''
        #problema()


if __name__ == "__main__":
    main()