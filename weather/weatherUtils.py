from typing import List
import pandas as pd

from pandas import DataFrame

from Objects.legObject import Leg

def appendTemps(legs: List[Leg], weather: DataFrame):
    hourly_weather = weather[weather['type'] == 'hourly']

    for leg in legs:
        leg.weather = hourly_weather[(hourly_weather['date'] >= leg.startTime  - pd.Timedelta(minutes=30)) 
                                     & (hourly_weather['date'] <= leg.finishTime + pd.Timedelta(minutes=30))]
        leg.minTemp = leg.weather['temperature_2m'].min()
        leg.maxTemp = leg.weather['temperature_2m'].max()
        leg.avgTemp = leg.weather['temperature_2m'].mean()
        
