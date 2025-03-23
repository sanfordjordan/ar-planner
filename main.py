from typing import List
from Objects.legObject import Leg
from Objects.raceInfoObject import RaceInfo
from csvReader import readFood, readLegs, readWeather
from clothes import getClothes
from Food.food import appendFoodNeeded
from gear import getTAGear, getGear
from printers import  compare_food_nutrients, print_leg_food, printEventWeather, printLegDetails, printLegWeather, printNextWeather, printPrevWeather, printShoppingList, printWaterRequirements
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
    cleanupGear = getTAGear(legs)
    
    #Build Leg data
    for index, leg in enumerate(legs):
        print(leg.number, index, leg.discipline)

        clothes = getClothes(leg)
        gear = getGear(leg)
        prevLeg = legs[index - 1] if index > 0 else 'NA'
        if index == 14:
            print(leg.discipline)
            print(f"Weather for Leg {leg.number} between {leg.startTime} and {leg.finishTime}:")
            print(leg.weather[['date', 'temperature_2m', 'apparent_temperature', 'precipitation', 'precipitation_probability']])
            printLegWeather(leg)
     
        #food
        #water

    #printLegDetails(legs)
    #printWaterRequirements(legs)
    #print_leg_food(legs)
    #compare_food_nutrients(targets, actuals)
    #printShoppingList(legs)
    #printPrevWeather(weather)
    #printEventWeather(weather, raceInfo)
    #printNextWeather(legs[8].weather)

if __name__ == "__main__":
    main()