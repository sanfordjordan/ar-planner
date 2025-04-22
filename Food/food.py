from datetime import timedelta
import math
from typing import List, Tuple
from Food.noDoze import appendNoDoze
from Objects.foodObject import Food
from Objects.legObject import Leg
from Objects.userObject import User
from utils import getThing
from water import appendWaterNeeded

def appendFoodNeeded(legs: List[Leg], foodData: List[Food], user: User):
    appendNoDoze(legs)
    targets = []
    actuals = []

    for leg in legs:
        time = leg.avgTime
        target = createFoodTarget(time, user.foodFormula)
        caloriesNeeded = calcCalories(target)

        #Real food
        food = getRealFood(leg, user)
        realNutrients = calcActualNutrients(food,  foodData)
        realCalories = calcCalories(realNutrients)
        

        #Super juice
        caloriesToGo = caloriesNeeded - realCalories
        if caloriesToGo > 0 and leg.discipline != 'TA':
            SJInfo = getThing('4hr fuel', foodData)
            SJCalories = calcCalories(SJInfo)
            SJRequired = round(caloriesToGo / SJCalories, 1)
            food.append((SJInfo.name, SJRequired))
        totalNutrients = calcActualNutrients(food,  foodData)


        #Spare super juice
        spareSJ = round(time/12, 1) #SJ for 1/3 the leg length (/4 as it lasts 4hrs)

        #Salt
        saltNeeded = target.sodium - totalNutrients.sodium
        if saltNeeded > 0 and leg.discipline != 'TA':
            saltInfo = getThing('SaltStick Caps 100', foodData)
            saltPillsNeeded = round(saltNeeded/saltInfo.sodium)
            if saltPillsNeeded > 0: food.append((saltInfo.name, saltPillsNeeded))
            totalNutrients = calcActualNutrients(food,  foodData)

        #Water
        waterFromFood = totalNutrients.water
        appendWaterNeeded(leg, user, waterFromFood)
        

        # Chlorine pills
        waterToClean = leg.waterReq - 3
        if waterToClean > 0:
            pills = waterToClean / 2
            food.append(('chlorine tab', math.ceil(pills)))
       
        leg.food = food
        if leg.discipline != 'TA':
            leg.spareSJ = spareSJ
        
        targets.append(target)
        actuals.append(totalNutrients)
    
    return targets, actuals

def getRealFood(leg: Leg, user: User) -> List[str]:
    food = []
    optionsTable = []
    if leg.discipline == 'Kayak': optionsTable = user.kayakFood
    elif leg.discipline == 'Bike': optionsTable = user.bikeFood
    elif leg.discipline == 'Hike': optionsTable = user.hikeFood
   
    hours = round(leg.avgTime)
    if len(optionsTable) == 0: 
        if leg.discipline == 'TA':
            food.append('unc toby chewy apricot bar')
            if hours > 2: food.append('Tuna mexican rice')
    elif len(optionsTable) <= hours: food = optionsTable[-1]
    else: food = optionsTable[hours-1]
    food = [food for food in food if food != '4hr fuel'] #not real food, add it on later
    return countFood(food)

def countFood(realFood: List[str]) -> List[Tuple[str, int]]:
    food_count = {}
    
    # Count the occurrences of each food in the list
    for food in realFood:
        if food in food_count:
            food_count[food] += 1
        else:
            food_count[food] = 1
    
    # Convert the dictionary to a list of tuples
    return [(food, count) for food, count in food_count.items()]

def createFoodTarget(time: timedelta, foodFormula: list) -> Food:
    n = [value * time for value in foodFormula]
    return Food(['target', 0, 0, 0, n[2], n[1], n[0], 0, 50, 30, 0, 235, n[3], 0, 0])

def calcCalories(food: Food) -> float: return (food.carbs * 4) + (food.protein * 4) + (food.fat * 9) 


def calcActualNutrients(foodNeeded: list, foodData: List[Food]):
    foodActual =  Food(['target', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    foodNames = ['carbs', 'protein', 'fat', 'sodium', 'magnesium', 'potassium', 'calcium', 'water']

    for foodItem in foodNeeded:
        itemInfo = getThing(foodItem[0], foodData)
        for nutrient in foodNames:
            setattr(foodActual, nutrient, getattr(foodActual, nutrient) + getattr(itemInfo, nutrient) * foodItem[1])
    return foodActual

def nutrient_difference(self, other):
    # Calculate differences in each nutrient
    return {
        'calories': round(calcCalories(self) - calcCalories(other)),
        'carbs': round(self.carbs - other.carbs),
        'protein': round(self.protein - other.protein),
        'fat': round(self.fat - other.fat),
        'sodium': round(self.sodium - other.sodium),

    }
