import csv
from typing import List, Tuple
from Objects.legObject import Leg
from Objects.raceInfoObject import RaceInfo
from datetime import datetime

def readCSV()-> Tuple[List[Leg], RaceInfo]:
    inputData = []
    startTime = ''
    location = ''

    with open('input.csv', mode ='r')as file:
        csvFile = csv.reader(file)
        for index, line in enumerate(csvFile):
            if index == 1:
                startTime = line[0]
                startDate = line[1]
                location = line[2]
                startDateTime = datetime.strptime(f"{startDate} {startTime}", "%d/%m/%Y %H:%M")
                raceInfo = RaceInfo(startDateTime, location)
                
            if index >= 3:
                inputData.append(Leg(line))
                
    return inputData, raceInfo

