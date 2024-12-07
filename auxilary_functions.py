import pandas as pd
from io import StringIO

from weather_codes import weather_conditions

def gen_table(data, classes=''):
    table = pd.read_json(StringIO(data)).to_html(border=1,header=False,escape=False,classes=classes)
    return table

# this creates a separate html table with weather descriptions and corresponding icons
# could be use to add a separte row with weather tiles for each day
def get_weather_icons(json):
    df = pd.DataFrame(pd.read_json(StringIO(json)))
    weather = df.iloc[-1]
    icon_and_desc = [weather_conditions.get(str(code), ['unknown', 'unknown']) for code in weather]
    icon_ids = [element[0] for element in icon_and_desc]
    descriptions = [element[1] for element in icon_and_desc]
    table = pd.DataFrame([icon_ids, descriptions]).to_html(border=0,header=False,index=False,escape=False)
    return table

def get_icons(weather_codes):
    icon_and_desc = [weather_conditions.get(str(code), ['unknown', 'unknown']) for code in weather_codes]
    icons = [element[0] for element in icon_and_desc]
    descriptions = [element[1] for element in icon_and_desc]
    return icons, descriptions