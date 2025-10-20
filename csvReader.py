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

def readLegs()-> Tuple[List[Leg], RaceInfo]:
    legs = []

    with open('DB/legsDB.csv', mode ='r')as file:
        csvFile = csv.reader(file)
        for index, line in enumerate(csvFile):
            if line[0] == '': break
            if index == 1:
                raceInfo = RaceInfo(line)

            if index >= 3:
                if index > 3:
                    legs.append(Leg([int(line[0])-1, 'TA', 0, 0, 0, line[5], 0]))
                legs.append(Leg(line))
    
    legs[0].boxes = Box('bike, paddle, A, B, C, D')
    return legs, raceInfo

def readFood()-> Tuple[List[Leg], RaceInfo]:
    foodData = []

    with open('DB/foodDB.csv', mode ='r')as file:
        csvFile = csv.reader(file)
        for index, line in enumerate(csvFile):
            if index > 0:
                foodData.append(Food(line))
    return foodData

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

