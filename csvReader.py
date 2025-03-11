import csv

from legObject import Leg
from timeUtils import calcTime
from datetime import datetime

def readCSV():
    inputData = []
    startTime = ''
    location = ''
    prevSleptNight = None

    with open('input.csv', mode ='r')as file:
        csvFile = csv.reader(file)
        for index, line in enumerate(csvFile):
            if index == 1:
                startTime = line[0]
                startDate = line[1]
                startDateTime = datetime.strptime(f"{startDate} {startTime}", "%d/%m/%Y %H:%M")
                location = line[2]
            if index >= 3:
                leg = Leg(line)
                prevLeg = 'NA'
                if index > 3: prevLeg = inputData[-1]
                currentStart, currentFinish, prevSleptNight, didSleep = calcTime(prevLeg, leg, startDateTime, prevSleptNight)
                leg.startTime = currentStart
                leg.finishTime = currentFinish
                leg.sleepBefore = didSleep
                inputData.append(leg)
                #missing weather data, time estimates
                
    return inputData

