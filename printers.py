import pandas as pd
import matplotlib.pyplot as plt

from datetime import datetime, timedelta
from collections import defaultdict
from typing import List
from Food.food import nutrient_difference
from Objects.foodObject import Food
from Objects.legObject import Leg
from Objects.raceInfoObject import RaceInfo

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

def printPrevWeather(df):
    df['date'] = pd.to_datetime(df['date'])
    today = datetime.now().date()
    one_week_ago = today - timedelta(days=7)
    last_week_df = df[(df['date'].dt.date >= one_week_ago) & (df['date'].dt.date <= today)]
    printWeatherDaily(last_week_df, 'Weather Last Week')

def printEventWeather(df, raceInfo: RaceInfo):
    df['date'] = pd.to_datetime(df['date'])
    start = raceInfo.startDateTime.date()
    end = raceInfo.finishDateTime.date()
    eventDF = df[(df['date'].dt.date >=start) & (df['date'].dt.date <= end)]
    printWeatherHourly(eventDF, 'Weather During Event')

def printWeatherDaily(dfSegment, title):
    # Extract necessary columns
    dates = dfSegment['date']
    min_temps = dfSegment['temperature_2m_min']
    max_temps = dfSegment['temperature_2m_max']
    rainfall = dfSegment['precipitation_sum']

    # Plotting
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Temperature plot with fill_between
    ax1.fill_between(dates, min_temps, max_temps, color='lightcoral', alpha=0.5, label='Temperature Range')
    ax1.plot(dates, min_temps, color='blue', linestyle='--', label='Min Temperature')
    ax1.plot(dates, max_temps, color='red', linestyle='--', label='Max Temperature')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Temperature (°C)')
    ax1.set_title(title)
    ax1.legend(loc='upper left')
    ax1.grid(True)

    # Rainfall plot on secondary y-axis
    ax2 = ax1.twinx()
    ax2.bar(dates, rainfall, color='skyblue', alpha=0.6, width=0.6, label='Rainfall')
    ax2.set_ylabel('Rainfall (mm)')
    ax2.legend(loc='upper right')

    # Formatting x-axis for better readability
    fig.autofmt_xdate()

    plt.show()

def printWeatherHourly(df, title):
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Plot apparent temperature
    ax1.plot(df['date'], df['apparent_temperature'], 'b-', marker='o', label='Apparent Temperature (°C)')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Apparent Temperature (°C)', color='b')
    ax1.tick_params('y', colors='b')

    # Create a second y-axis for precipitation
    ax2 = ax1.twinx()
    ax2.bar(df['date'], df['precipitation'], color='gray', alpha=0.3, label='Precipitation (mm)')
    ax2.set_ylabel('Precipitation (mm)', color='gray')
    ax2.tick_params('y', colors='gray')

    # Add precipitation probability as a line plot
    ax3 = ax1.twinx()
    ax3.plot(df['date'], df['precipitation_probability'], 'g--', marker='x', label='Precipitation Probability (%)')
    ax3.set_ylabel('Precipitation Probability (%)', color='g')
    ax3.tick_params('y', colors='g')
    ax3.spines['right'].set_position(('outward', 60))  # Offset the third y-axis

    # Add legends
    fig.legend(loc='upper left', bbox_to_anchor=(0.1, 0.9))

    # Format x-axis
    plt.gcf().autofmt_xdate()

    plt.title(title)
    plt.show()