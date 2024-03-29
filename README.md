# WeatherCat
---
## CS 1998 App Challenge 2019

### What our app does:
<p>WeatherCat is a visual representation of the weather by showing how a cartoon
cat is dressed for the weather.</p>

### Screenshots
<img src="screenshots/screen1.png" width="50%" height="50%">
<img src="screenshots/screen2.png" width="50%" height="50%">

### Repositories:
<p>Frontend: <a href="https://github.com/jasmineherrera/weathercat-ios">
https://github.com/jasmineherrera/weathercat-ios
</a></p>
<p>Backend: <a href="https://github.com/Weather-Cat/appchallenge">
https://github.com/Weather-Cat/appchallenge
</a></p>
<p>Docker Image: <a href="https://hub.docker.com/r/gaiagirl007/weathercat">
https://hub.docker.com/r/gaiagirl007/weathercat
</a></p>

### Description:
<p>
This app makes requests to a server along the routes specified in app.py, which
then makes requests to an external API, openweathermap.org, to get the weather
and forecast data used in this app.
</p>
<p>
Based on either a city or a set of coordinates and selected units, the app makes a
request to the API which determines and populates various fields, including current
temperature, daily high, daily low, humidity, wind speed, wind direction, and the current
weather conditions. The current temperature is compared to the temperature range
of each cat in the CatWear table from db.py. Which range the current temperature
is in determines which cat is appropriate for the weather.
</p>
<p>
A second request is then made, (based on the same coordinates and units) which
determines the high and low temperatures for the next 3 days, as well as the 3-hourly
changes in temperature and weather conditions for the next 12 hours.
</p>
<p>
Both the weather and forecast information is returned to the app, which presents
the information to the user.
</p>

### Backend requirements:
<ol>
<li>Designed an API (app.py) using Flask routes and queries to a database (db.py)
to store and process information</li>
<li>SQLAlchemy used to model how the cat information is stored (temperature range
for the image in both Fahrenheit and Celcius and the image name)</li>
<li>Currently running on a Docker container inside of a Google Cloud Server</li>
</ol>
