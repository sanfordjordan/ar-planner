import csv
import os
import pandas as pd

from typing import List, Tuple
from Objects.boxesObject import Box
from Objects.foodObject import Food
from Objects.gearObject import Gear
from Objects.legObject import Leg
from Objects.raceInfoObject import RaceInfo

from datetime import datetime, timedelta
from weather.weather import callWeatherMan

def read_legs() -> Tuple[List[Leg], RaceInfo]:
    legs = []
    race_info = None

    with open('DB/legsDB.csv', mode='r') as file:
        csv_file = csv.reader(file)
        for index, line in enumerate(csv_file):
            if line[0] == '': break
            if index == 1:
                race_info = RaceInfo(line)
            if index >= 3:
                leg = Leg(line)
                if index == 3:
                    leg.boxes = Box('bike, paddle, A, B, C, D')
                legs.append(leg)

    return legs, race_info

def read_food_data() -> List[Food]:
    food_data = []

    with open('DB/foodDB.csv', mode='r') as file:
        csv_file = csv.reader(file)
        next(csv_file)  # Skip the header
        for line in csv_file:
            food_data.append(Food(line))

    return food_data

def readWeather() -> pd.DataFrame:
    weatherCSV = 'DB/weather.csv'
    if isRecent(weatherCSV):
        print("📄 Reading weather data from CSV...")
        df = pd.read_csv(weatherCSV, parse_dates=['date'])
        df['date'] = pd.to_datetime(df['date'])
    else:
        print("🌐 Fetching weather data from API...")
        daily_df, hourly_df = callWeatherMan()
   
        # Concatenate with multi-index headers (optional, simplifies re-load later)
        daily_df['type'] = 'daily'
        hourly_df['type'] = 'hourly'
        combined_df = pd.concat([daily_df, hourly_df], ignore_index=True)

        combined_df.to_csv(weatherCSV, index=False)
        df = combined_df
    return df

def readGear()-> List[Gear]:
    gearList = []

    with open('DB/gearDB.csv', mode ='r')as file:
        csvFile = csv.reader(file)
        for index, line in enumerate(csvFile):
            if index >= 1:
                gearList.append(Gear(line))
                
    return gearList


# Check if recent
def isRecent(filepath):
    override = False
    if not os.path.exists(filepath) or override:
        return False
    mod_time = datetime.fromtimestamp(os.path.getmtime(filepath))
    return (datetime.now() - mod_time) < timedelta(hours=1)

