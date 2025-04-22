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
    inputData = []
    startTime = ''
    latitude = ''

    with open('DB/legsDB.csv', mode ='r')as file:
        csvFile = csv.reader(file)
        for index, line in enumerate(csvFile):
            if index == 1:
                startTime = line[0]
                startDate = line[1]
                latitude = line[2]
                longitude = line[3]
                startDateTime = datetime.strptime(f"{startDate} {startTime}", "%d/%m/%Y %H:%M")
                raceInfo = RaceInfo(startDateTime, latitude, longitude)

            if index >= 3:
                if index > 3:
                    TAInfo = [int(line[0])-1, 'TA', '', '', 0, line[5], '']
                    inputData.append(Leg(TAInfo))
                inputData.append(Leg(line))
                
    return inputData, raceInfo

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

        # Save to CSV
        combined_df.to_csv(weatherCSV, index=False)
        df = combined_df
    # df now holds the weather data
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

