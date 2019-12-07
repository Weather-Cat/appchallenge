import json
import os
import requests
import dao
import time
from secrets import *
from flask import Flask, request
from db import db, User, CatWear

db_filename = "wxcat.db"
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % db_filename
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db.init_app(app)
with app.app_context():
    db.create_all()

#Default route, just there to see if the API works :)
@app.route('/')
def welcome():
    return "You've reached the WeatherCat API!"

#initialize the databases used for decision making
@app.route('/api/initialize/')
def initialize_cats():
    try:
        cats = dao.init_catwear()
        return json.dumps({'success': True, 'data': cats}), 201

    except:
        return json.dumps({'success': False, 'error': "CatWear database still uninitalized :("}), 404



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

#get the current location
#probably will be replaced with something on front end side
# @app.route('/api/location/')
# def get_current_location():
#     """Connects to an external API to find the current coordinates of the user and
#     returns a json object that includes:
#     {
#     "success": true,
#     "data": {
#         "latitude": <number>,
#         "longitude": <number>
#         }
#     }
#     May need information to be sent with the request for the API? If so keep as
#     GET and include info in route or change to POST?"""
#     pass

#define a new location for the user
#DO NOT IMPLEMENT NOW!
# @app.route('/api/location/new/', methods = ['POST'])
# def new_location():
#     """Inserts a new location into the locations database. Requests must look like:
#     {
#     "latitude": <number>,
#     "longitude": <number>,
#     "location_name": <string>,
#     "user": <something here?>
#     }
#     Returns a json object that includes:
#     {
#     "success": true,
#     "data": <serialized location>
#     }
#     The serialized version of the location includes id, closest city, and
#     coordinates."""
#     pass

#get a location for the user
#DO NOT IMPLEMENT NOW!
# @app.route('/api/location/<int:locationid>/')
# def get_saved_location(locationid):
#     """Gets a location from the locations database. Returns a json object that includes:
#     {
#     "success": true,
#     "data": <serialized location>
#     }
#     The serialized version of the location includes id, closest city, and
#     coordinates"""
#     pass

#delete one of the user's locations
#DO NOT IMPLEMENT NOW!
# @app.route('/api/location/delete/<int:locationid>/', methods = ['DELETE'])
# def delete_location(locationid):
#     """Deletes a location from the locations database. Returns a json object
#     that includes:
#     {
#     "success": true,
#     "data": <serialized location>
#     }
#     The serialized version of the location includes id, closest city, and
#     coordinates"""
#     pass

#acesses an external API to get the current weather for the user's location
@app.route('/api/weather/', methods = ['POST'])
@app.route('/api/weather', methods = ['POST'])
#@app.route('/api/weather/<int:locationid>/', methods = ['POST'])
def get_wx(locationid = 0):
    """Acesses the current weather for a given location. A locationid of 0
    indicates that the weather for the given coordinates should be accessed.
    """
    try:
        pbody = json.loads(request.data)
        units = pbody.get('units')
        lat = pbody.get('latitude')
        lon = pbody.get('longitude')
        data = requests.get(ADDR+WX+'?lat='+str(lat)+'&lon='+str(lon)+'&units='+units+APIKEY)
        data = data.json()

        temp = data['main']['temp']
        humidity = data['main']['humidity']
        t_max = data['main']['temp_max']
        t_min = data['main']['temp_min']
        wind = {'speed': data['wind']['speed'], 'dir': data['wind']['deg']}
        weather = [{'name': i['main'],
            'icon_route': ICON + i['icon'] + '.png'
            } for i in data['weather']]

        wind['dir'] = dao.convert_wind(wind['dir'])
        cat = dao.get_catwear(temp)
        if cat == 'error':
            return json.dumps({'success': False, 'error': 'cat not found'}), 404

        return json.dumps({
            'success': True,
            'data': {
                "latitude": lat,
                "longitude": lon,
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
#@app.route('/api/forecast/<int:locationid>/', methods = ['POST'])
def get_forecast(locationid = 0):
    """Acesses the forecast for a given location. A locationid of 0 indicates
    that the forecast for the given coordinates should be accessed.
    """
    try:
        pbody = json.loads(request.data)
        units = pbody.get('units')
        lat = pbody.get('latitude')
        lon = pbody.get('longitude')
        local_time = pbody.get('local_time')
        data = requests.get(ADDR+FCST+'?lat='+str(lat)+'&lon='+str(lon)+'&units='+units+APIKEY)
        data = data.json()

        all_t = []
        times = []
        for d in data['list']:
            all_t.append(d['main']['temp'])
            times.append(d['dt_txt'])

        highlow = dao.high_lows(all_t, times, local_time)
        return json.dumps({
            'success': True,
            'data': {
                "latitude": lat,
                "longitude": lon,
                "units": units,
                "high_temps": highlow[0],
                "low_temps": highlow[1]
            }}), 200

    except:
        return json.dumps({'success': False, 'error': 'forecast not found'}), 404


if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5000, debug = True)
