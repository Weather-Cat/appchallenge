import json
import os
import requests
import dao
import time
from flask import Flask, request
from db import db, User, CatWear
from dotenv import load_dotenv, find_dotenv

db_filename = "wxcat.db"
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % db_filename
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db.init_app(app)
with app.app_context():
    db.create_all()

load_dotenv(find_dotenv())

APIKEY = os.getenv("APIKEY")
ADDR = os.getenv("ADDR")
WX = os.getenv("WX")
ICON = os.getenv("ICON")
FCST = os.getenv("FCST")

#Default route, just there to see if the API works :)
@app.route('/')
def welcome():
    return "You've reached the WeatherCat API!"

#initialize the databases used for decision making
@app.route('/api/initialize/')
def initialize_cats():
    catwear = CatWear.query.all()
    if len(catwear) == 0:
        try:
            dao.init_catwear()
            catwear = CatWear.query.all()
            res = [s.serialize() for s in catwear]
            return json.dumps({'success': True, 'data': res}), 201
        except:
            return json.dumps({'success': False, 'error': "CatWear database still uninitalized"}), 404
    else:
        return json.dumps({'success': False, 'error': "CatWear database is already initialized"}) , 404


@app.route('/api/user/', methods = ['POST'])
def new_user():
    try:
        pbody = json.loads(request.data)
        user = User(username = pbody.get('username'))
        db.session.add(user)
        db.session.commit()
        return json.dumps({'success': True, 'data': user.serialize()}), 200
    except:
        return json.dumps({'success': False, 'error': 'Could not create user'}), 404


@app.route('/api/user/<int:userid>/')
def get_user(userid):
    try:
        user = User.query.filter_by(id = userid).first()
        return json.dumps({'success': True, 'data': user.serialize()}), 201
    except:
        return json.dumps({'success': False, 'error': 'user not found'}), 404


@app.route('/api/user/<int:userid>/delete/', methods = ['DELETE'])
def delete_user(userid):
    try:
        user = User.query.filter_by(id = userid).first()
        db.session.delete(user)
        db.session.commit()
        return json.dumps({'success': True, 'data': user.serialize()}), 200
    except:
        return json.dumps({'success': False, 'error': 'user not found'}), 404


#acesses an external API to get the current weather for the user's location
@app.route('/api/weather/', methods = ['POST'])
@app.route('/api/weather', methods = ['POST'])
def get_wx():
    """Acesses the current weather for a given location."""
    try:
        args = request.args
        pbody = json.loads(request.data)
        units = pbody.get('units')
        lat = pbody.get('latitude', None)
        lon = pbody.get('longitude', None)
        city = args.get('city', None)
        if lat != None and lon != None:
            location = '?lat='+str(lat)+'&lon='+str(lon)
            city = None

        elif city != None:
            location = '?q='+str(city)
        else:
            return json.dumps({'success': False, 'error': 'missing location'}), 404

        data = requests.get(ADDR+WX+location+'&units='+units+APIKEY)
        data = data.json()

        temp = data['main']['temp']
        humidity = data['main']['humidity']
        t_max = data['main']['temp_max']
        t_min = data['main']['temp_min']
        wind = {'speed': data['wind']['speed'], 'dir': data['wind']['deg']}
        weather = [{'name': i['main'],
            'icon_route': ICON+i['icon']+'.png'
            } for i in data['weather']]

        if city != None:
            lat = data['coord']['lat']
            lon = data['coord']['lon']

        wind['dir'] = dao.convert_wind(wind['dir'])
        cat = dao.get_catwear(temp, units)
        if cat == 'error':
            return json.dumps({'success': False, 'error': 'cat not found'}), 404

        return json.dumps({
            'success': True,
            'data': {
                "latitude": lat,
                "longitude": lon,
                "city": city,
                "units": units,
                "temp": temp,
                "temp_max": t_max,
                "temp_min": t_min,
                "humidity": humidity,
                "wind": wind,
                "weather": weather,
                "cat": cat
            }}), 200

    except:
        return json.dumps({'success': False, 'error': 'weather not found'}), 404

#acesses an external API to get the forecasted weather for the user's location
@app.route('/api/forecast/', methods = ['POST'])
@app.route('/api/forecast', methods = ['POST'])
def get_forecast():
    """Acesses the forecast for a given location."""
    try:
        args = request.args
        pbody = json.loads(request.data)
        units = pbody.get('units')
        lat = pbody.get('latitude', None)
        lon = pbody.get('longitude', None)
        city = args.get('city', None)

        if lat != None and lon != None:
            location = '?lat='+str(lat)+'&lon='+str(lon)
            city = None

        elif city != None:
            location = '?q='+str(city)
        else:
            return json.dumps({'success': False, 'error': 'request missing location'}), 404

        data = requests.get(ADDR+FCST+location+'&units='+units+APIKEY)
        data = data.json()

        if city != None:
            lat = data['city']['coord']['lat']
            lon = data['city']['coord']['lon']

        all_t = []
        times = []
        weather = []
        i = 0
        for d in data['list']:
            all_t.append(d['main']['temp'])
            times.append(d['dt_txt'])
            if i < 4:
                weather.append([{'name': w['main'], 'icon_route': ICON+w['icon']+'.png'} for w in d['weather']])
                i+=1

        tz = data['city']['timezone']
        highlow = dao.high_lows(all_t, times, tz)
        forecast_12hr = highlow['12hr_forecast']
        for hour in range(len(weather)):
            forecast_12hr[hour]['weather'] = weather[hour]

        return json.dumps({
            'success': True,
            'data': {
                "latitude": lat,
                "longitude": lon,
                "city": city,
                "units": units,
                "high_temps": highlow['highs'],
                "low_temps": highlow['lows'],
                "twelvehrforecast": forecast_12hr
            }}), 200

    except:
        return json.dumps({'success': False, 'error': 'forecast not found'}), 404


if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5000, debug = True)
