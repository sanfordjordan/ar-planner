from collections import defaultdict
from typing import List
from Food.food import nutrient_difference
from Objects.foodObject import Food
from Objects.legObject import Leg

def printWaterRequirements(inputData: List[Leg]):
    total_water = sum(leg.waterReq for leg in inputData if leg.discipline != 'TA')

    print("\n" + "=" * 60)
    print(f"{'Leg':<5} | {'Discipline':<12} | {'Avg Temp (°C)':<14} | {'Avg Time (hrs)':<16} | {'Water Req (L)':<12}")
    print("-" * 60)

    for leg in inputData:
        if leg.discipline == 'TA': continue  # Skip TA legs
        print(f"{leg.number:<5} | {leg.discipline:<12} | {leg.avgTemp:<14.1f} | {leg.avgTime:<16.2f} | {leg.waterReq:<12.2f}")

    print("-" * 60)
    print(f"{'Total':<35} | {'':<16} | {total_water:<12.2f}")
    print("=" * 60 + "\n")

def printLegDetails(inputData: List[Leg]):
    for leg in inputData:
        if (leg.discipline == "TA"):
            print(f"  TA Duration: {str(leg.finishTime - leg.startTime)}")
        else:
            print(f"Leg {leg.number}: {leg.discipline}")
            print(f"  Start Time:  {leg.startTime.strftime('%A')} {leg.startTime.strftime('%H:%M')}")
            print(f"  Finish Time: {leg.finishTime.strftime('%A')} {leg.finishTime.strftime('%H:%M')}")
            print(f"  Duration:    {leg.avgTime:.2f} hours")
   

        print("-" * 40)

# Function to compare the nutrient values
def compare_food_nutrients(targets: List[Food], actuals: List[Food]):
    overall_diff = {'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0, 'sodium': 0}
    
    print(f"{'Food':<10}{'Calories Diff':<15}{'Carbs Diff':<15}{'Protein Diff':<15}{'Fat Diff':<15}{'Sodium Diff':<15}")
    print('-' * 80)
    
    leg_count = 1
    for index, (target, actual) in enumerate(zip(targets, actuals)):
        if index % 2 != 0: continue
        
        diff = nutrient_difference(actual, target)
        leg_label = f"Leg {leg_count}"
        leg_count += 1
        
        print(f"{leg_label:<10}{diff['calories']:<15}{diff['carbs']:<15}{diff['protein']:<15}{diff['fat']:<15}{diff['sodium']:<15}")
        
        for nutrient in overall_diff: overall_diff[nutrient] += diff[nutrient]
    
    print('-' * 80)
    print(f"{'Total Dif':<10}{overall_diff['calories']:<15}{overall_diff['carbs']:<15}{overall_diff['protein']:<15}{overall_diff['fat']:<15}{overall_diff['sodium']:<15}")

def print_leg_food(legs: List[Leg]):
    print(f"{'Leg/TA':<10}{'Food Item':<35}{'Amount':<10}")
    print("-" * 55)
    
    for index, leg in enumerate(legs):
        legOrTA = f"Leg {(index // 2) + 1}" if index % 2 == 0 else f"TA {(index // 2) + 1}"
        
        if not leg.food:
            print(f"{legOrTA:<10}{'(No Food)':<35}")
            continue
        
        first_item = True
        for food_name, amount in leg.food:
            if amount < 0: continue
            
            if first_item:
                print(f"{legOrTA:<10}{food_name:<35}{amount:<10}")
                first_item = False
            else:
                print(f"{'':<10}{food_name:<35}{amount:<10}")  # Indent food items below the leg/TA label

        print("-" * 55)


def printShoppingList(legs: List[Leg]):
    shopping_list = defaultdict(float)

    for leg in legs:
        for food_item, quantity in leg.food:
            shopping_list[food_item] += quantity

    sorted_items = sorted(shopping_list.items())

    print(f"{'Item':<30}{'Total Quantity'}")
    print('-' * 45)

    for item, total in sorted_items:
        if item.lower() in ['4hr fuel']: qty_display = round(total, 1)
        else: qty_display = int(total)
        print(f"{item:<30}{qty_display}")

    print('-' * 45)
    print(f"Total unique items: {len(sorted_items)}")