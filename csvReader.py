import csv
from typing import List, Tuple
from Objects.boxesObject import Box
from Objects.foodObject import Food
from Objects.legObject import Leg
from Objects.raceInfoObject import RaceInfo
from datetime import datetime

def readLegs()-> Tuple[List[Leg], RaceInfo]:
    inputData = []
    startTime = ''
    location = ''

    with open('DB/legsDB.csv', mode ='r')as file:
        csvFile = csv.reader(file)
        for index, line in enumerate(csvFile):
            if index == 1:
                startTime = line[0]
                startDate = line[1]
                location = line[2]
                startDateTime = datetime.strptime(f"{startDate} {startTime}", "%d/%m/%Y %H:%M")
                raceInfo = RaceInfo(startDateTime, location)

            if index >= 3:
                if index > 3:
                    TAInfo = [index-3, 'TA', '', '', 0, Box(line[5]), '']
                    inputData.append(Leg(TAInfo))
                inputData.append(Leg(line))
                
    return inputData, raceInfo

def readFood()-> Tuple[List[Leg], RaceInfo]:
    foodData = []

    with open('DB/foodDB.csv', mode ='r')as file:
        csvFile = csv.reader(file)
        for index, line in enumerate(csvFile):
            if index > 0:
                foodData.append(Food(line))
    return foodData

