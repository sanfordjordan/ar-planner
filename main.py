from typing import List
from Objects.legObject import Leg
from Objects.raceInfoObject import RaceInfo
from csvReader import readCSV
from clothes import getClothes
from gear import getCleanupGear, getGear
from printers import  printLegDetails, printWaterRequirements
from timeUtils import appendTimes
from water import appendWaterNeeded

sweatLevel = 1

def main():
    legsData, raceInfo = readCSV()
    legsData = appendTimes(legsData, raceInfo)
    #legsData = appendTemps(legsData, raceInfo) TODO

  
    
    #Build Leg data
    for index, leg in enumerate(legsData):
        appendWaterNeeded(leg, sweatLevel)

        clothes = getClothes(leg)
        gear = getGear(leg)
        prevLeg = legsData[index - 1] if index > 0 else 'NA'
        cleanupGear = getCleanupGear(prevLeg)
        
        #gear for cleaning up after prev leg
        #food
        #water
        #sleep gear

    printLegDetails(legsData)
    printWaterRequirements(legsData)

if __name__ == "__main__":
    main()