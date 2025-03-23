import matplotlib.dates as mdates
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
    today = datetime.now().date()
    one_week_ago = today - timedelta(days=7)
    last_week_df = df[(df['date'].dt.date >= one_week_ago) & (df['date'].dt.date <= today)]
    printWeatherDaily(last_week_df, 'Weather Last Week')

def printEventWeather(df, raceInfo: RaceInfo):
    start = raceInfo.startDateTime.date()
    end = raceInfo.finishDateTime.date()
    eventDF = df[(df['date'].dt.date >=start) & (df['date'].dt.date <= end)]
    printWeatherHourly(eventDF, 'Weather During Event')

def printNextWeather(df):
    start = datetime.now().date()
    end =  start + timedelta(days=7)
    eventDF = df[(df['date'].dt.date >=start) & (df['date'].dt.date <= end)]
    printWeatherHourly(eventDF, 'Weather This Week')

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
    fig, ax1 = plt.subplots(figsize=(15, 7))
    
    # Plot Actual and Apparent Temperature on ax1
    ax1.plot(df['date'], df['temperature_2m'], color='blue', marker='o', label='Actual Temperature')
    ax1.plot(df['date'], df['apparent_temperature'], color='red', linestyle='--', marker='x', label='Apparent Temperature')
    ax1.set_xlabel("Date and Time")
    ax1.set_ylabel("Temperature (°C)", color='black')
    ax1.tick_params(axis='y', labelcolor='black')
    
    # Create a secondary axis for precipitation and probability
    ax2 = ax1.twinx()
    ax2.bar(df['date'], df['precipitation'], color='gray', alpha=0.4, width=0.03, label='Precipitation (mm)')
    ax2.plot(df['date'], df['precipitation_probability'], color='green', linestyle=':', marker='s', label='Precipitation Probability (%)')
    ax2.set_ylabel("Precipitation / Probability", color='black')
    ax2.tick_params(axis='y', labelcolor='black')
    
    ax1.set_xticks(df['date'][::3])
    ax1.set_xticklabels([dt.strftime('%H') for dt in df['date'][::3]], rotation=45)


    
    # Mark vertical lines at the start of each day in the filtered data
    # Get unique days (as datetime with time 00:00:00)
    unique_days = pd.to_datetime(df['date'].dt.date.unique())
    for day in unique_days:
        ax1.axvline(day, color='purple', linestyle='--', alpha=0.5)
        # Annotate the day near the top
        ax1.text(day, ax1.get_ylim()[1], day.strftime('%a %b %d'), 
                 rotation=90, verticalalignment='bottom', color='purple', fontsize=8)
    
    # Combine legends from both axes
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
    
    plt.title(title)
    plt.gcf().autofmt_xdate()  # Auto-format date labels
    plt.tight_layout()
    plt.show()