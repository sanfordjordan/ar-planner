import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry

def callWeatherMan():
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": -37.74993839269664,
        "longitude": 144.9364853643536,
        "daily": ["sunshine_duration", "rain_sum", "precipitation_probability_max", "temperature_2m_max", "sunrise", "showers_sum", "sunset", "temperature_2m_min", "apparent_temperature_max", "apparent_temperature_min", "precipitation_hours", "precipitation_sum", "daylight_duration"],
        "hourly": ["temperature_2m", "precipitation_probability", "precipitation", "rain", "showers", "cloud_cover", "cloud_cover_high", "cloud_cover_mid", "cloud_cover_low", "wind_speed_10m", "wind_direction_10m", "wind_direction_180m", "temperature_180m", "is_day", "apparent_temperature"],
        "timezone": "Australia/Sydney",
        "past_days": 7,
        "forecast_days": 16,
    }
    responses = openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]

    # Process hourly data. The order of variables needs to be the same as requested.
    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
    hourly_precipitation_probability = hourly.Variables(1).ValuesAsNumpy()
    hourly_precipitation = hourly.Variables(2).ValuesAsNumpy()
    hourly_rain = hourly.Variables(3).ValuesAsNumpy()
    hourly_showers = hourly.Variables(4).ValuesAsNumpy()
    hourly_cloud_cover = hourly.Variables(5).ValuesAsNumpy()
    hourly_cloud_cover_high = hourly.Variables(6).ValuesAsNumpy()
    hourly_cloud_cover_mid = hourly.Variables(7).ValuesAsNumpy()
    hourly_cloud_cover_low = hourly.Variables(8).ValuesAsNumpy()
    hourly_wind_speed_10m = hourly.Variables(9).ValuesAsNumpy()
    hourly_wind_direction_10m = hourly.Variables(10).ValuesAsNumpy()
    hourly_wind_direction_180m = hourly.Variables(11).ValuesAsNumpy()
    hourly_temperature_180m = hourly.Variables(12).ValuesAsNumpy()
    hourly_is_day = hourly.Variables(13).ValuesAsNumpy()
    hourly_apparent_temperature = hourly.Variables(14).ValuesAsNumpy()

    hourly_data = {"date": pd.date_range(
        start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
        end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
        freq = pd.Timedelta(seconds = hourly.Interval()),
        inclusive = "left"
    )}

    hourly_data['date'] = pd.to_datetime(hourly_data['date'], utc=True)
    hourly_data['date'] = hourly_data['date'].tz_convert('Australia/Sydney')
    hourly_data['date'] = hourly_data['date'].tz_localize(None)
    hourly_data["temperature_2m"] = hourly_temperature_2m
    hourly_data["precipitation_probability"] = hourly_precipitation_probability
    hourly_data["precipitation"] = hourly_precipitation
    hourly_data["rain"] = hourly_rain
    hourly_data["showers"] = hourly_showers
    hourly_data["cloud_cover"] = hourly_cloud_cover
    hourly_data["cloud_cover_high"] = hourly_cloud_cover_high
    hourly_data["cloud_cover_mid"] = hourly_cloud_cover_mid
    hourly_data["cloud_cover_low"] = hourly_cloud_cover_low
    hourly_data["wind_speed_10m"] = hourly_wind_speed_10m
    hourly_data["wind_direction_10m"] = hourly_wind_direction_10m
    hourly_data["wind_direction_180m"] = hourly_wind_direction_180m
    hourly_data["temperature_180m"] = hourly_temperature_180m
    hourly_data["is_day"] = hourly_is_day
    hourly_data["apparent_temperature"] = hourly_apparent_temperature

    hourly_dataframe = pd.DataFrame(data = hourly_data)

    # Process daily data. The order of variables needs to be the same as requested.
    daily = response.Daily()
    daily_sunshine_duration = daily.Variables(0).ValuesAsNumpy()
    daily_rain_sum = daily.Variables(1).ValuesAsNumpy()
    daily_precipitation_probability_max = daily.Variables(2).ValuesAsNumpy()
    daily_temperature_2m_max = daily.Variables(3).ValuesAsNumpy()
    daily_sunrise = daily.Variables(4).ValuesAsNumpy()
    daily_showers_sum = daily.Variables(5).ValuesAsNumpy()
    daily_sunset = daily.Variables(6).ValuesAsNumpy()
    daily_temperature_2m_min = daily.Variables(7).ValuesAsNumpy()
    daily_apparent_temperature_max = daily.Variables(8).ValuesAsNumpy()
    daily_apparent_temperature_min = daily.Variables(9).ValuesAsNumpy()
    daily_precipitation_hours = daily.Variables(10).ValuesAsNumpy()
    daily_precipitation_sum = daily.Variables(11).ValuesAsNumpy()
    daily_daylight_duration = daily.Variables(12).ValuesAsNumpy()

    daily_data = {"date": pd.date_range(
        start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
        end = pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
        freq = pd.Timedelta(seconds = daily.Interval()),
        inclusive = "left"
    )}
    daily_data['date'] = pd.to_datetime(daily_data['date'], utc=True)
    daily_data['date'] = daily_data['date'].tz_convert('Australia/Sydney')
    daily_data['date'] = daily_data['date'].tz_localize(None)
    daily_data["sunshine_duration"] = daily_sunshine_duration
    daily_data["rain_sum"] = daily_rain_sum
    daily_data["precipitation_probability_max"] = daily_precipitation_probability_max
    daily_data["temperature_2m_max"] = daily_temperature_2m_max
    daily_data["sunrise"] = daily_sunrise
    daily_data["showers_sum"] = daily_showers_sum
    daily_data["sunset"] = daily_sunset
    daily_data["temperature_2m_min"] = daily_temperature_2m_min
    daily_data["apparent_temperature_max"] = daily_apparent_temperature_max
    daily_data["apparent_temperature_min"] = daily_apparent_temperature_min
    daily_data["precipitation_hours"] = daily_precipitation_hours
    daily_data["precipitation_sum"] = daily_precipitation_sum
    daily_data["daylight_duration"] = daily_daylight_duration

    daily_dataframe = pd.DataFrame(data = daily_data)
    return daily_dataframe, hourly_dataframe

