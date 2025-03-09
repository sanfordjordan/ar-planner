import sys

from csvReader import readCSV
from clothes import getClothes
from gear import getGear

def main():
    inputData = readCSV()
    
    for leg in inputData:
        clothes = getClothes(leg)
        gear = getGear(leg)
        #gear for cleaning up after prev leg
        #food
        #water
        #sleep gear
        print(clothes)


if __name__ == "__main__":
    main()