import requests
import numpy as np
import json
import pandas as pd
from io import StringIO
from datetime import datetime

from weather_codes import weather_conditions
from auxilary_functions import get_icons

defaultLatitude = 21
defaultLongitude = 37

def validate_input_coordinates(lat: float, long: float):
    if not (-90 <= lat <= 90):
        raise ValueError("Invalid latitude. Must be between -90 and 90.")
    if not (-180 <= long <= 180):
        raise ValueError("Invalid longitude. Must be between -180 and 180.")

def forecast(lat=defaultLatitude,long=defaultLongitude):
    #input validation and data sourcing
    validate_input_coordinates(lat,long)
    endpoint_1 = "https://api.open-meteo.com/v1/forecast?latitude={}&longitude={}&daily=temperature_2m_max,temperature_2m_min,daylight_duration,weather_code&timezone=Europe/Warsaw"
    response = requests.get(endpoint_1.format(lat,long))
    data = response.json()

    #calculations
    max_temperatures = data['daily']['temperature_2m_max']
    min_temperatures = data['daily']['temperature_2m_min']
    weather_codes = data['daily']['weather_code']
    icons, descriptions = get_icons(weather_codes)
    dates = [datetime.strptime(date, "%Y-%m-%d").strftime("%d/%m/%Y") for date in data['daily']['time']]
    installation_capacity_kW = 2.5
    panel_efficiency = 0.2
    sun_exposure = data['daily']['daylight_duration']
    generated_power = [installation_capacity_kW * panel_efficiency * sunlight / 3600 for sunlight in sun_exposure] #seconds need to be converted to h
    
    #final data assembly
    final_data = {
                i:{
                    "Date": dates[i],
                    "Max temperature [C]": max_temperatures[i],
                    "Min temperature [C]": min_temperatures[i],
                    "Projected power generation [kWh]": round(generated_power[i], 3),
                    "Weather code": weather_codes[i],
                    "Weather icon": icons[i],
                    "Weather description": descriptions[i]
                }
                for i in range(len(dates))
                }
    final_data = json.dumps(final_data, indent=4)
    return final_data

def week_summary(lat=defaultLatitude,long=defaultLongitude):
    #input validation and data sourcing
    validate_input_coordinates(lat,long)
    endpoint_2 = "https://api.open-meteo.com/v1/forecast?latitude={}&longitude={}&daily=temperature_2m_max,temperature_2m_min,daylight_duration,weather_code&hourly=surface_pressure&timezone=Europe/Warsaw"
    response = requests.get(endpoint_2.format(lat,long))
    data = response.json()

    #calculations
    avg_pressure = round(np.mean(data['hourly']['surface_pressure']), 3)
    max_temp = np.max(data['daily']['temperature_2m_max'])
    min_temp = np.min(data['daily']['temperature_2m_min'])
    weather_codes = data['daily']['weather_code']
    dates = [datetime.strptime(date, "%Y-%m-%d").strftime("%d/%m/%Y") for date in data['daily']['time']]
    daylight = data['daily']['daylight_duration']
    avg_sun_exposure = f'{round(np.mean(daylight)) // 3600}:{(round(np.mean((daylight))) % 3600) // 60}'

    #asigning codes to 'rainy' or 'sunny' weather values
    keywords = ['rain', 'drizzle', 'freezing rain', 'thunderstorm']
    rain_codes = [int(code) for code, description in weather_conditions.items() if any(word in description for word in keywords)]
    
    rainy_days, sunny_days = 0, 0
    for code in weather_codes:
        if code in rain_codes:
            rainy_days += 1
        elif code in [0,1]:
            sunny_days += 1
    
    #final data assembly
    final_data = {
                    0:{
                        "Date": dates[0] + " to " + dates[-1], 
                        "Max weekly temperature [C]": max_temp, 
                        "Min weekly temperature [C]": min_temp, 
                        "Average sunlight exposure [h:min]": avg_sun_exposure, 
                        "Average pressure [hPa]": avg_pressure, 
                        "Sunny/rainy days during the week": f'{sunny_days}/{rainy_days}'
                        }
                }
    final_data = json.dumps(final_data, indent=4)
    return final_data
