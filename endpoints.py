import requests
import numpy as np
import json
import pandas as pd
from io import StringIO

from weather_codes import weather_conditions

forcast_length = 7

def validate_input_coordinates(lat: float, long: float):
    if not (-90 <= lat <= 90):
        raise ValueError("Invalid latitude. Must be between -90 and 90.")
    if not (-180 <= long <= 180):
        raise ValueError("Invalid longitude. Must be between -180 and 180.")

def forecast(lat=21.37,long=69.):
    validate_input_coordinates(lat,long)
    endpoint_1 = "https://api.open-meteo.com/v1/forecast?latitude={}&longitude={}&daily=temperature_2m_max,temperature_2m_min,daylight_duration,weather_code&timezone=Europe/Warsaw"
    response = requests.get(endpoint_1.format(lat,long))
    data = response.json()

    max_temperatures = data['daily']['temperature_2m_max']
    min_temperatures = data['daily']['temperature_2m_min']
    weather_codes = data['daily']['weather_code']
    dates = data['daily']['time']
    installation_capacity_kW = 2.5
    panel_efficiency = 0.2
    sun_exposure = data['daily']['daylight_duration']
    generated_power = [installation_capacity_kW * panel_efficiency * sunlight / 3600 for sunlight in sun_exposure] #seconds need to be converted to h
    
    final_data = {
                i:{
                    "date": dates[i],
                    "max_temperature": max_temperatures[i],
                    "min_temperature": min_temperatures[i],
                    "projected_power_generation": round(generated_power[i], 3),
                    "weather_code": weather_codes[i]
                }
                for i in range(len(dates))
                }
    final_data = json.dumps(final_data, indent=4)
    return final_data

def week_summary(lat=21.37,long=69.):
    validate_input_coordinates(lat,long)
    endpoint_2 = "https://api.open-meteo.com/v1/forecast?latitude={}&longitude={}&daily=temperature_2m_max,temperature_2m_min,daylight_duration,weather_code&hourly=surface_pressure&timezone=Europe/Warsaw"
    response = requests.get(endpoint_2.format(lat,long))
    data = response.json()

    avg_pressure = round(np.mean(data['hourly']['surface_pressure']), 3)
    max_temp = np.max(data['daily']['temperature_2m_max'])
    min_temp = np.min(data['daily']['temperature_2m_min'])
    weather_codes = data['daily']['weather_code']
    dates = data['daily']['time']
    avg_sun_exposure = round(np.mean(data['daily']['daylight_duration'])/3600, 3)

    keywords = ['rain', 'drizzle', 'freezing rain', 'thunderstorm']
    rain_codes = [int(code) for code, description in weather_conditions.items() if any(word in description for word in keywords)]
    
    rainy_days, sunny_days = 0, 0
    for code in weather_codes:
        if code in rain_codes:
            rainy_days += 1
        elif code in [0,1]:
            sunny_days += 1
    
    final_data = {
                    0:{
                        "date": "from " + dates[0] + " to " + dates[-1], 
                        "max_weekly_temperature": max_temp, 
                        "min_weekly_temperature": min_temp, 
                        "average_weekly_sunlight_exposure": avg_sun_exposure, 
                        "average_weekly_pressure": avg_pressure, 
                        "sunny_days/rainy_days": f'{sunny_days}/{rainy_days}'
                        }
                }
    final_data = json.dumps(final_data, indent=4)
    return final_data

def gen_table(data):
    table = pd.read_json(StringIO(data)).to_html(border=1,header=False)
    return table

def get_weather_icons(json):
    df = pd.DataFrame(pd.read_json(StringIO(json)))
    weather = df.iloc[-1]
    icon_and_desc = [weather_conditions.get(str(code), ['unknown', 'unknown']) for code in weather]
    icon_ids = [element[0] for element in icon_and_desc]
    descriptions = [element[1] for element in icon_and_desc]
    table = pd.DataFrame([icon_ids, descriptions]).to_html(border=0,header=False,index=False,escape=False)
    return table