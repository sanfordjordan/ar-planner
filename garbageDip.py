import itertools
import math
from typing import List
from Objects.foodObject import Food


def update_nutrient_totals(food, amount, carb_actual, protein_actual, fat_actual, sodium_actual, magnesium_actual, potassium_actual, calcium_actual):
    """
    Helper method to update the nutrient totals based on the food item and amount consumed.
    """
    carb_actual += food.kJ * amount
    protein_actual += food.protein * amount
    fat_actual += food.fat * amount
    sodium_actual += food.sodium * amount
    magnesium_actual += food.magnesium * amount
    potassium_actual += food.potassium * amount
    calcium_actual += food.calcium * amount
    return carb_actual, protein_actual, fat_actual, sodium_actual, magnesium_actual, potassium_actual, calcium_actual


def find_best_food_combo2(target: Food, foodData: List[Food]):
    food_options = ['Jamwich', 'Banana', 'clif bar', 'unc toby chewy apricot bar', 'oreo minis', 'chips']
    carbTarget = target.carbs / 3
    fatTarget = target.fat / 3
    proteinTarget = target.protein / 3
    best_combo = None
    best_diff = float('inf')

    # Generate all combinations of food items with possible quantities (e.g., 0 to 5 of each item)
    # Change the range(6) depending on how many of each item you can have
    max_quantity = 5  # You can adjust this based on how many of each item you want to consider
    # We create a list of all possible quantities of each food (from 0 to max_quantity)
    quantity_ranges = [range(max_quantity + 1)] * len(food_options)

    # Iterate through all possible combinations of quantities for each food item
    for quantities in itertools.product(*quantity_ranges):
        total_carbs = 0
        total_protein = 0
        total_fat = 0

        # Calculate the total carbs, protein, and fat for this combination of quantities
        for i, quantity in enumerate(quantities):
            food_name = food_options[i]
            itemInfo = next(food for food in foodData if food.name == food_name)
            total_carbs += itemInfo.carbs * quantity
            total_protein += itemInfo.protein * quantity
            total_fat += itemInfo.fat * quantity

        # Calculate the difference between the target and the current combination
        diff = math.sqrt((total_carbs - carbTarget)**2 + 
                         (total_protein -proteinTarget)**2 + 
                         (total_fat - fatTarget)**2)

        # Update the best combination if this one is closer to the target
        if diff < best_diff:
            best_diff = diff
            best_combo = quantities

    # Return the best combination found, and the total nutrition values for that combo
    best_food_combo = []
    total_carbs = 0
    total_protein = 0
    total_fat = 0
    for i, quantity in enumerate(best_combo):
        if quantity > 0:
            food = foodData[i]
            best_food_combo.append((food.name, quantity))
            total_carbs += food.carbs * quantity
            total_protein += food.protein * quantity
            total_fat += food.fat * quantity

    return best_food_combo, total_carbs, total_protein, total_fat
    
def cokedUpRn(leg, raceInfo, legsData, foodData):
        i = 0
            # COKE: not day 1, only when leg passes between midnight and 10am, not when sleep is imminent
        if leg.startTime.date() > raceInfo.startDateTime.date():
            # Check if it's a night leg between midnight and 10 AM
               if (leg.startTime < leg.startTime.replace(hour=10, minute=0, second=0, microsecond=0)) or \
   (leg.startTime >= leg.startTime.replace(hour=21, minute=0, second=0, microsecond=0) and \
    (leg.finishTime < leg.finishTime.replace(hour=10, minute=0, second=0, microsecond=0) or \
     leg.finishTime.date() > leg.startTime.date())):
                # Determine if next leg is a TA and if you plan to sleep during it
                next_leg = legsData[i + 1] if i + 1 < len(legsData) else None
                
                # If next leg is a TA or there is no next leg and you're not sleeping during the next TA
                if not next_leg or (next_leg and next_leg.discipline == 'TA' and not next_leg.sleepDuring):
                    # If it's morning and you don't have sleep planned, you need Coke
                    coke = next(food for food in foodData if food.name =='coke (500mL)')
                    cokeAmount = 1.5 if (leg.finishTime - leg.startTime).total_seconds() / 3600 > 3 else 1
                    leg.foodNeeded.append((coke, cokeAmount))
                    