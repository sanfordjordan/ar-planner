import pprint
import matplotlib.dates as mdates
import pandas as pd
import matplotlib.pyplot as plt

from datetime import datetime, timedelta
from collections import defaultdict
from typing import List
from Food.food import nutrient_difference
from Objects.clothingObject import Clothing
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
            boxes = leg.boxes.boxesArray
            if boxes:
                print(f"  Boxes:    {', '.join(boxes)}")
            else:
                print("  Boxes:    none")
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

def printPrevWeather(weather):
    today = datetime.now().date()
    one_week_ago = today - timedelta(days=7)
    last_week_hWeather = weather[(weather['date'].dt.date >= one_week_ago) & (weather['date'].dt.date <= today)]
    printWeatherDaily(last_week_hWeather, 'Weather Last Week')

def printEventWeather(weather, raceInfo: RaceInfo):
    start = raceInfo.startDateTime.date()
    end = raceInfo.finishDateTime.date()
    eventhWeather = weather[(weather['date'].dt.date >=start) & (weather['date'].dt.date <= end)]
    printWeatherHourly(eventhWeather, 'Weather During Event')

def printNextWeather(weather):
    start = datetime.now().date()
    end =  start + timedelta(days=7)
    eventhWeather = weather[(weather['date'].dt.date >=start) & (weather['date'].dt.date <= end)]
    printWeatherHourly(eventhWeather, 'Weather This Week')

def printLegWeather(leg: Leg):
    title = f"Weather for Leg {leg.number} {leg.discipline} between {leg.startTime} and {leg.finishTime}"
    printWeatherHourly(leg.weather, title)

def printWeatherDaily(weather, title):
    dWeather = weather[weather['type'] == 'daily']

    # Extract necessary columns
    dates = dWeather['date']
    min_temps = dWeather['temperature_2m_min']
    max_temps = dWeather['temperature_2m_max']
    rainfall = dWeather['precipitation_sum']

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

def printWeatherHourly(weather, title):
    hWeather = weather[weather['type'] == 'hourly']
    fig, ax1 = plt.subplots(figsize=(15, 7))
    
    # Temperature and Wind Speed on ax1
    ax1.plot(hWeather['date'], hWeather['temperature_2m'], color='blue', marker='o', label='Actual Temperature')
    ax1.plot(hWeather['date'], hWeather['apparent_temperature'], color='red', linestyle='--', marker='x', label='Apparent Temperature')
    ax1.plot(hWeather['date'], hWeather['wind_speed_10m'], color='orange', linestyle='-.', label='Wind Speed (m/s)')
    ax1.set_xlabel("Time")
    ax1.set_ylabel("Temperature (°C) / Wind Speed (m/s)", color='black')
    ax1.tick_params(axis='y', labelcolor='black')
    ax1.set_ylim(0, 40)
    
    # Min & Max Temp annotations
    if not hWeather.empty:
        min_temp = hWeather['temperature_2m'].min()
        max_temp = hWeather['temperature_2m'].max()
        min_temp_time = hWeather['date'][hWeather['temperature_2m'].idxmin()]
        max_temp_time = hWeather['date'][hWeather['temperature_2m'].idxmax()]
        ax1.annotate(f'Min Temp: {min_temp}°C', xy=(min_temp_time, min_temp), xytext=(min_temp_time, min_temp + 2),
                     arrowprops=dict(facecolor='blue', arrowstyle='->'), fontsize=10, color='blue')
        ax1.annotate(f'Max Temp: {max_temp}°C', xy=(max_temp_time, max_temp), xytext=(max_temp_time, max_temp - 2),
                     arrowprops=dict(facecolor='red', arrowstyle='->'), fontsize=10, color='red')

    # Precipitation on ax2
    ax2 = ax1.twinx()
    ax2.bar(hWeather['date'], hWeather['precipitation'], color='deepskyblue', alpha=1, width=0.03, label='Precipitation (mm)')
    ax2.set_ylabel("Precipitation (mm)", color='deepskyblue')
    ax2.tick_params(axis='y', labelcolor='deepskyblue')
    ax2.set_ylim(0, 2)

    # Precipitation Probability on ax3
    ax3 = ax1.twinx()
    ax3.plot(hWeather['date'], hWeather['precipitation_probability'], color='green', linestyle=':', marker='s', label='Precipitation Probability (%)')
    ax3.spines['right'].set_position(('outward', 60))  # Move outwards to avoid overlap
    ax3.set_ylabel("Precipitation Probability (%)", color='green')
    ax3.tick_params(axis='y', labelcolor='green')
    ax3.set_ylim(0, 100)

    # Cloud Cover Bars at back
    ax4 = ax1.twinx()
    ax4.spines['right'].set_position(('outward', 120))  # Further out to avoid clutter
    for i, date in enumerate(hWeather['date']):
        ax4.bar(date, hWeather['cloud_cover'].iloc[i], 
                color='lightgray', 
                alpha=0.5,
                width=0.042, 
                zorder=-1)
    # Hide cloud cover axis
    ax4.spines['right'].set_visible(False)
    ax4.tick_params(axis='y', which='both', left=False, right=False, labelleft=False, labelright=False)

    # X-ticks every 3 hours
    ax1.set_xticks(hWeather['date'][::3])
    ax1.set_xticklabels([dt.strftime('%H') for dt in hWeather['date'][::3]], rotation=45)

    # Vertical lines for days
    unique_days = pd.to_datetime(hWeather['date'].dt.date.unique())
    for day in unique_days:
        ax1.axvline(day, color='purple', linestyle='--', alpha=0.5)
        ax1.text(day, ax1.get_ylim()[1], day.strftime('%a %b %d'), 
                 rotation=90, verticalalignment='bottom', color='purple', fontsize=8)
    
    # Add Cloud Cover to legend
    cloud_cover_patch = plt.Line2D([0], [0], color='lightgray', alpha=0.5, lw=4, label='Cloud Cover')
    
    # Combine all legends
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    lines3, labels3 = ax3.get_legend_handles_labels()
    ax1.legend(lines1 + lines2 + lines3 + [cloud_cover_patch], labels1 + labels2 + labels3 + ['Cloud Cover'], loc='upper left')

    # Title & Layout
    plt.title(title)
    plt.gcf().autofmt_xdate()
    plt.tight_layout()
    plt.show()


def printClothing(clothing: Clothing):
    print("----- Clothing To Wear -----")
    
    if clothing.head:
        print("🧢 Head:")
        for item in clothing.head:
            print(f"   - {item}")
    
    if clothing.body:
        print("👕 Body:")
        for item in clothing.body:
            print(f"   - {item}")
    
    if clothing.hand:
        print("🧤 Hands:")
        for item in clothing.hand:
            print(f"   - {item}")
    
    if clothing.legs:
        print("🩳 Legs:")
        for item in clothing.legs:
            print(f"   - {item}")
    
    if clothing.feet:
        print("👟 Feet:")
        for item in clothing.feet:
            print(f"   - {item}")
    
    print("------------------------")

def create_packing_lists(gear_array):
    # Initialize dictionaries for each box and starting gear
    packing_lists = {
        'starting gear': [],
        'bike box': [],
        'paddle bag': [],
        'box A': [],
        'box B': [],
        'box C': [],
        'box D': [],
        'leaveStuff': []
    }
    
    # Sort each item into appropriate list based on first journey entry
    for gear in gear_array:
        if gear.journey == []: continue
        initial_location = gear.journey[0]
        if initial_location in ['use', 'carry']:
            packing_lists['starting gear'].append(gear.name)
        else:
            box_name = {
                'bike': 'bike box',
                'paddle': 'paddle bag',
                'A': 'box A',
                'B': 'box B',
                'C': 'box C',
                'D': 'box D',
                'leaveStuff': 'leaveStuff'
            }.get(initial_location, initial_location)
            packing_lists[box_name].append(gear.name)
    
    # Print the lists
    print("\nPACKING LISTS")
    print("=============\n")
    
    for location, items in packing_lists.items():
        if items:  # Only print lists that have items
            print(f"{location.upper()}:")
            for item in sorted(items):  # Sort items alphabetically
                print(f"  - {item}")
            print()

