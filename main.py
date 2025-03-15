from typing import List
from Objects.legObject import Leg
from Objects.raceInfoObject import RaceInfo
from csvReader import readFood, readLegs
from clothes import getClothes
from Food.food import appendFoodNeeded
from gear import getCleanupGear, getGear
from printers import  compare_food_nutrients, printLegDetails, printWaterRequirements
from timeUtils import appendTimes
from users.createUser import createUser
from utils import set_user_value

userName = set_user_value('B')  # Or 'J'



def main():
    user = createUser(userName)
    legsData, raceInfo = readLegs()
    foodData = readFood()
    appendTimes(legsData, raceInfo)
    #appendTemps(legsData, raceInfo) TODO
    targets, actuals = appendFoodNeeded(legsData, foodData, user)
  
    
    #Build Leg data
    for index, leg in enumerate(legsData):
        

        clothes = getClothes(leg)
        gear = getGear(leg)
        prevLeg = legsData[index - 1] if index > 0 else 'NA'
        cleanupGear = getCleanupGear(prevLeg)
        #add TA info. maybe create obj? food and water during TA
        #gear for cleaning up after prev leg
        #food
        #water
        #sleep gear

    #printLegDetails(legsData)
    #printWaterRequirements(legsData)
    compare_food_nutrients(targets, actuals)

if __name__ == "__main__":
    main()