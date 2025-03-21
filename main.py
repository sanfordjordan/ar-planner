from typing import List
from Objects.legObject import Leg
from Objects.raceInfoObject import RaceInfo
from csvReader import readFood, readLegs, readWeather
from clothes import getClothes
from Food.food import appendFoodNeeded
from gear import getTAGear, getGear
from printers import  compare_food_nutrients, print_leg_food, printEventWeather, printLegDetails, printPrevWeather, printShoppingList, printWaterRequirements
from timeUtils import appendTimes
from users.createUser import createUser
from utils import set_user_value

userName = set_user_value('B')  # Or 'J'



def main():
    user = createUser(userName)
    legs, raceInfo = readLegs()
    foodData = readFood()
    appendTimes(legs, raceInfo)
    weather = readWeather()
    #printPrevWeather(weather)
    printEventWeather(weather, raceInfo)
    #appendTemps(legsData, raceInfo) TODO
    targets, actuals = appendFoodNeeded(legs, foodData, user)
    cleanupGear = getTAGear(legs)
    
    #Build Leg data
    for index, leg in enumerate(legs):
        

        clothes = getClothes(leg)
        gear = getGear(leg)
        prevLeg = legs[index - 1] if index > 0 else 'NA'
       
     
        #food
        #water

    #printLegDetails(legs)
    #printWaterRequirements(legs)
    #print_leg_food(legs)
    #compare_food_nutrients(targets, actuals)
    #printShoppingList(legs)

if __name__ == "__main__":
    main()