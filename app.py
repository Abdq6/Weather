from flask import Flask, render_template, request

from endpoints import week_summary, forecast, gen_table, get_weather_icons

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/forecast', methods=['GET'])
def get_forecast():
    latitude = float(request.args.get('lat'))
    longitude = float(request.args.get('long'))
    result = forecast(latitude,longitude)
    icon_table = get_weather_icons(result)
    tabular_data = gen_table(result)
    return icon_table + tabular_data

@app.route('/summary', methods=['GET'])
def get_week_summary():
    latitude = float(request.args.get('lat'))
    longitude = float(request.args.get('long'))
    tabular_summary = gen_table(week_summary(latitude,longitude))
    return tabular_summary


if __name__ == '__main__':
    app.run()
