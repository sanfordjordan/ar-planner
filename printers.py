from typing import List
from Food.food import nutrient_difference
from Objects.foodObject import Food
from Objects.legObject import Leg

def printWaterRequirements(inputData: List[Leg]):
    total_water = sum(leg.waterReq for leg in inputData)

    print("\n" + "=" * 60)
    print(f"{'Leg':<5} | {'Discipline':<12} | {'Avg Temp (°C)':<14} | {'Avg Time (hrs)':<16} | {'Water Req (L)':<12}")
    print("-" * 60)

    for index, leg in enumerate(inputData, start=1):
        print(f"{index:<5} | {leg.discipline:<12} | {leg.avgTemp:<14.1f} | {leg.avgTime:<16.2f} | {leg.waterReq:<12.2f}")

    print("-" * 60)
    print(f"{'Total':<35} | {'':<16} | {total_water:<12.2f}")
    print("=" * 60 + "\n")

def printLegDetails(inputData: List[Leg]):
    leg_counter = 0  # Track actual legs (excluding TA's)

    for leg in inputData:
        isTA = (leg.discipline == "TA")

        if isTA:
            print(f"  TA Duration: {str(leg.finishTime - leg.startTime)}")
        else:
            leg_counter += 1
            print(f"Leg {leg_counter}: {leg.discipline}")
            print(f"  Start Time:  {leg.startTime.strftime('%A')} {leg.startTime.strftime('%H:%M')}")
            print(f"  Finish Time: {leg.finishTime.strftime('%A')} {leg.finishTime.strftime('%H:%M')}")
            print(f"  Duration:    {leg.avgTime:.2f} hours")
   

        print("-" * 40)

# Function to compare the nutrient values
def compare_food_nutrients(targets: List[Food], actuals: List[Food]):
    overall_diff = {'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0, 'sodium': 0}
    
    # Print headers for the comparison table
    print(f"{'Food':<20}{'Calories Diff':<15}{'Carbs Diff':<15}{'Protein Diff':<15}{'Fat Diff':<15}{'Sodium Diff':<15}")
    print('-' * 95)
    
    for index, (target, actual) in enumerate(zip(targets, actuals)):
        diff = nutrient_difference(actual, target)
        
        leg_or_ta = f"Leg {(index // 2) + 1}" if index % 2 == 0 else f"TA {(index // 2) + 1}"
        print(f"{leg_or_ta:<20}{diff['calories']:<15}{diff['carbs']:<15}{diff['protein']:<15}{diff['fat']:<15}{diff['sodium']:<15}")
        
        for nutrient in overall_diff:
            overall_diff[nutrient] += diff[nutrient]
    
    # Print the overall comparison
    print('-' * 95)
    print(f"{'Total Dif':<20}{overall_diff['calories']:<15}{overall_diff['carbs']:<15}{overall_diff['protein']:<15}{overall_diff['fat']:<15}{overall_diff['sodium']:<15}")
