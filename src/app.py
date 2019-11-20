import json
import os
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

#get the current location
@app.route('/api/location/')
def get_current_location():
    """Connects to an external API to find the current coordinates of the user and
    returns a json object that includes:
    {
    "success": true,
    "data": {
        "latitude": <number>,
        "longitude": <number>
        }
    }
    May need information to be sent with the request for the API? If so keep as
    GET and include info in route or change to POST?"""
    pass

#define a new location for the user
#DO NOT IMPLEMENT NOW!
@app.route('/api/location/new/', methods = ['POST'])
def new_location():
    """Inserts a new location into the locations database. Requests must look like:
    {
    "latitude": <number>,
    "longitude": <number>,
    "location_name": <string>,
    "user": <something here?>
    }
    Returns a json object that includes:
    {
    "success": true,
    "data": <serialized location>
    }
    The serialized version of the location includes id, closest city, and
    coordinates."""
    pass

#get a location for the user
#DO NOT IMPLEMENT NOW!
@app.route('/api/location/<int:locationid>/')
def get_saved_location(locationid):
    """Gets a location from the locations database. Returns a json object that includes:
    {
    "success": true,
    "data": <serialized location>
    }
    The serialized version of the location includes id, closest city, and
    coordinates"""
    pass

#delete one of the user's locations
#DO NOT IMPLEMENT NOW!
@app.route('/api/location/delete/<int:locationid>/', methods = ['DELETE'])
def delete_location(locationid):
    """Deletes a location from the locations database. Returns a json object
    that includes:
    {
    "success": true,
    "data": <serialized location>
    }
    The serialized version of the location includes id, closest city, and
    coordinates"""
    pass

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
    "units": <string, e or m (english or metric)>
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
        "current_weather": <list of strings>,
        "cat_wears": <serialized version of what the cat is wearing>,
        "background": <list of serialized version of background elements>
        }
    }
    """
    pass

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
        "prob_of_precip": <list of 4 int, see above>
        }
    }
    """
    pass


if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5000, debug = True)
