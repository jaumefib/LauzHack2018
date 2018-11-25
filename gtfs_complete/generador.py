#! /usr/bin/python3
import random
from sys import argv

def makeFile():
    noms = ["stops","transfers","routes","trips","stop_times"]
    atributs = [["Id","Col","Name","Col","Lat","Lon"],["From","To","Kind","Time"],
        ["Id","Col","Col","Name","Col","Type"],["Route","Col","Id"],["Trip","Col","Col","Id"]]
    idStops = [0,1,2,3,4,5]
    col = "0"
    nameStops = ["A","B","C","D","E","F"]
    #Lat = Lon = random.randint(1, 100)
    fromTransfer =
    toTransfer =
    kindTransport = [2,2,2]
    time = random.randint(15,120)
    nameRoute = ["R1","R2","R3"]
    tripsRoute =
    idRoute =
    tripStopTimes =
    idStopTimes =
	for i in noms:
		fileName = noms[i] + ".txt"

        text = atributs[i,:]

		print(text, file=open(fileName, "w"))

        if noms[i] == "stops":
            for j in range(0:6):
                print(nameStops[j]+","+col+","+nameStops[j]+","+col+","+
                    str(random.randint(1,100))+","+str(random.randint(1,100)),
                    end='',file=open(fileName,"a"))
        if noms[i] == "transfers":
            for j in range(0:6):
                print(nameStops[random.randint(0,6)]
                    end='',file=open(fileName,"a"))


		print("", end='', file=open(fileName, "a"))

		print("", file=open(fileName, "a"))

def __ini__ = "__main__":
    makeFile()