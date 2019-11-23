import json
import os
import requests
from secrets import *
from flask import Flask, request

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

@app.route('/api/user/', methods = ['POST'])
def new_user():
    try:
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
def get_user(userid):
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
#@app.route('/api/weather/<int:locationid>/', methods = ['POST'])
def get_wx(locationid = 0):
    """Acesses the current weather for a given location. A locationid of 0
    indicates that the weather for the given coordinates should be accessed. The
    POST body should be:
    {
    "latitude": <number>,
    "longitude": <number>,
    "units": <string, imperial or metric>
    }
    Returns a json object that includes:
    {
    "success": true,
    "data": {
        "latitude": <number>,
        "longitude": <number>,
        "units": <string, e or m (english or metric)>,
        "temperature": <int>,
        "wind": <list of one int (speed) and one string (direction)>,
        "weather": <list of strings>,
        "cat_wears": <serialized version of what the cat is wearing>,
        "background": <list of serialized version of background elements>
        }
    }
    """
    try:
        units = pbody.get('units')
        lat = pbody.get('latitude')
        lon = pbody.get('longitude')
        data = requests.get(WXADDR + '?lat=' + lat + '&lon=' + lon + APIKEY)

        temp = data['main'].get('temp')
        humidity = data['main'].get('humidity')
        t_max = data['main'].get('temp_max')
        t_min = data['main'].get('temp_min')
        wind = {'speed': data['wind'].get('speed'), 'dir': data['wind'].get('deg')}
        weather = {'wx_id': data['weather'].get('id'), 'description': data['weather'].get('description')}

        if wind['dir'] > 337.5 or wind['dir'] <= 22.5:
            wind['dir'] = 'N'
        elif wind['dir'] > 22.5 or wind['dir'] <= 67.5:
            wind['dir'] = 'NE'
        elif wind['dir'] > 67.5 or wind['dir'] <= 112.5:
            wind['dir'] = 'E'
        elif wind['dir'] > 112.5 or wind['dir'] <= 157.5:
            wind['dir'] = 'SE'
        elif wind['dir'] > 157.5 or wind['dir'] <= 202.5:
            wind['dir'] = 'S'
        elif wind['dir'] > 202.5 or wind['dir'] <= 247.5:
            wind['dir'] = 'SW'
        elif wind['dir'] > 247.5 or wind['dir'] <= 292.5:
            wind['dir'] = 'W'
        elif wind['dir'] > 292.5 or wind['dir'] <= 337.5:
            wind['dir'] = 'NW'
        else:
            wind['dir'] = None

        return json.dumps({
            'success': True,
            'data': {
                "latitude": lat,
                "longitude": lon,
                "units": units,
                "temperature": temp,
                "high_temperature": t_max,
                "low_temperature": t_min,
                "humidity": humidity,
                "wind": wind,
                "weather": weather
                #cat part will be added later, once that database is initalized with values
            }}), 200

    except:
        return json.dumps({'success': False, 'error': 'weather not found'}), 404

#acesses an external API to get the forecasted weather for the user's location
@app.route('/api/forecast/', methods = ['POST'])
#@app.route('/api/forecast/<int:locationid>/', methods = ['POST'])
def get_forecast(locationid = 0):
    """Acesses the forecast for a given location. A locationid of 0 indicates
    that the forecast for the given coordinates should be accessed. The POST
    body should be:
    {
    "latitude": <number>,
    "longitude": <number>,
    "units": <string, e or m (english or metric)>
    }
    Returns a json object that includes:
    {
    "success": true,
    "data": {
        "units": <string, e or m (english or metric)>,
        "high_temperatures": <list of 4 int, index0=today, index1=tommorow, etc>,
        "low_temperatures": <list of 4 int, see above>
        }
    }
    """
    pass


if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5000, debug = True)
