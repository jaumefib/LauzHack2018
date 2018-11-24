actStation = 0

def insertStation(station, lon, lat, peopleIn, peopleOut):
    global actStation
    actStation = actStation + 1
    return actStation

def insertWalkable(idIn, idOut):
    return True

def insertLink(idIn, idOut, line, frequencies, people, kind, price):
    return True
