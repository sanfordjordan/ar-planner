from typing import List
from Objects.legObject import Leg
from Objects.raceInfoObject import RaceInfo
from csvReader import readFood, readLegs
from clothes import getClothes
from food import appendFoodNeeded
from gear import getCleanupGear, getGear
from printers import  printLegDetails, printWaterRequirements
from timeUtils import appendTimes
from water import appendWaterNeeded

sweatLevel = 1
weight = 57
#            carb, protein, fat, sodium, magnesium, potassium, calcium
foodFormula = [45, 5,       2.1, 400,    30,        235,       50] #TODO:formula based off weight

def main():
    legsData, raceInfo = readLegs()
    foodData = readFood()
    
    legsData = appendTimes(legsData, raceInfo)
    #legsData = appendTemps(legsData, raceInfo) TODO

  
    
    #Build Leg data
    for index, leg in enumerate(legsData):
        appendWaterNeeded(leg, sweatLevel)
        appendFoodNeeded(leg, weight)

        clothes = getClothes(leg)
        gear = getGear(leg)
        prevLeg = legsData[index - 1] if index > 0 else 'NA'
        cleanupGear = getCleanupGear(prevLeg)
        #add TA info. maybe create obj? food and water during TA
        #gear for cleaning up after prev leg
        #food
        #water
        #sleep gear

    printLegDetails(legsData)
    printWaterRequirements(legsData)

if __name__ == "__main__":
    main()