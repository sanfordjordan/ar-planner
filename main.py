from typing import List
from Objects.legObject import Leg
from Objects.raceInfoObject import RaceInfo
from charge import calcTorchBatteries
from csvReader import readFood, readLegs, readWeather
from clothes import appendClothes
from Food.food import appendFoodNeeded
from gear import appendTAGear, appendGear
from gearBoxes import calcBoxes
from printers import  compare_food_nutrients, print_leg_food, printClothing, printEventWeather, printLegDetails, printLegWeather, printNextWeather, printPrevWeather, printShoppingList, printWaterRequirements
from stepsTA import calcAllTASteps
from timeUtils import appendTimes
from users.createUser import createUser
from utils import set_user_value
from weather.weatherUtils import appendTemps

userName = set_user_value('B')  # Or 'J'



def main():
    user = createUser(userName)
    legs, raceInfo = readLegs()
    foodData = readFood()
    appendTimes(legs, raceInfo)
    weather = readWeather()
    appendTemps(legs, weather)
    targets, actuals = appendFoodNeeded(legs, foodData, user)
    calcTorchBatteries(legs)
    appendTAGear(legs)

    for index, leg in enumerate(legs):
        if leg.discipline != 'TA': 
            appendClothes(leg)
            appendGear(leg)
    calcBoxes(legs) 
    calcAllTASteps(legs)
    
    for index, leg in enumerate(legs):
       print(leg.number, leg.discipline, leg.batteries)
       
    #printLegDetails(legs)
    #printWaterRequirements(legs)
    #print_leg_food(legs)
    #printClothing(legs[0].clothing)
    #compare_food_nutrients(targets, actuals)
    #printShoppingList(legs)
    #printPrevWeather(weather)
    #printEventWeather(weather, raceInfo)
    #printNextWeather(legs[8].weather)
    #printLegWeather(legs[0])

if __name__ == "__main__":
    main()