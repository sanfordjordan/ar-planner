import csv

from legObject import Leg

def readCSV():
    inputData = []
    with open('input.csv', mode ='r')as file:
        csvFile = csv.reader(file)
        startTime = '8:30'
        #location = csvFile[1]
        print(startTime)
        index = 0
        for lines in csvFile: #TODO ignore first 3 lines
            if lines[0] != 'Leg': #skip title row
                leg = Leg(lines)
                prevLeg = 'NA'
                if index > 0: prevLeg = inputData(-1)
                currentStart, currentFinish = calcTime(prevLeg, leg, startTime)
                leg.startTime = currentStart
                leg.finishTime = currentFinish
                inputData.append(leg)
                #missing weather data, time estimates
                
    return inputData

def calcTime(prevLeg, currentLeg, startTime):
    currentDiscipline = currentLeg.discipline
  
    sleep = 0
    currentStart = startTime
    if prevLeg != 'NA': 
        taTime = 10
        lastDiscipline = prevLeg.discipline
        if lastDiscipline == 'Kayak': taTime += 10 
        if lastDiscipline == 'Bike': taTime += 6
        if currentDiscipline == 'Kayak': taTime += 8
        if currentDiscipline == 'Bike': taTime += 6
        currentStart = prevLeg.finishTime + taTime + sleep
        
    currentLegTimeEst = (currentLeg.shortTime + currentLeg.shortTime)# /2 #TODO string to time
    currentFinish = currentStart + currentLegTimeEst
    return (currentStart, currentFinish)
    #start time is prev finish + ta time + sleep
    