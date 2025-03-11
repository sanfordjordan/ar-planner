from typing import List
from legObject import Leg
from csvReader import readCSV
from clothes import getClothes
from gear import getGear
from timeUtils import printLegDetails

def main():
    inputData: List[Leg] = []
    inputData = readCSV()
    printLegDetails(inputData)

    for leg in inputData:
        clothes = getClothes(leg)
        gear = getGear(leg)
        #gear for cleaning up after prev leg
        #food
        #water
        #sleep gear

    

if __name__ == "__main__":
    main()