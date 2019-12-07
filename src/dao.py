from db import db, User, CatWear
from datetime import datetime, timezone, timedelta

def convert_wind(dir):
    """Converts a given wind direction in degrees to a cardinal direction (N, NW,
    W, etc)

    dir: 0 <= number <= 360
    """
    assert type(dir) in [float, int] and dir <= 360 and dir >= 0

    if dir > 337.5 or dir <= 22.5:
        dir = 'N'
    elif dir > 22.5 or dir <= 67.5:
        dir = 'NE'
    elif dir > 67.5 or dir <= 112.5:
        dir = 'E'
    elif dir > 112.5 or dir <= 157.5:
        dir = 'SE'
    elif dir > 157.5 or dir <= 202.5:
        dir = 'S'
    elif dir > 202.5 or dir <= 247.5:
        dir = 'SW'
    elif dir > 247.5 or dir <= 292.5:
        dir = 'W'
    elif dir > 292.5 or dir <= 337.5:
        dir = 'NW'
    else:
        dir = None

    return dir


def high_lows(temps, times, local_time):
    """Sorts out the highs and lows for a given block of temperatures. Also
    captures the local time and temperature for the first four items. Returns a
    dictionary, {"highs": [], "lows": [], "12hr_forecast": [list of dict]).

    temps: list of numbers
    times: list of dates/times in str format
    local_time: data/time in str format
    """
    assert is_number_list(temps)
    assert is_string_list(times)
    assert type(local_time) == str

    times = clean_times(times)
    length = len(times)
    local_now = clean_times(local_time, False)[0]
    utc_now = datetime.now(timezone.utc)
    offset = utc_now.hour - local_now.hour

    last_midnight = -1
    first4 = 0
    forecast_12hr = []
    highs = []
    i_highs = []
    lows = []
    for t in range(length):
        local = (times[t].hour - offset) % 24
        #scoop off the local time and the temperature for the first 4 time/temperature pairs
        if first4 < 4:
            forecast_12hr.append({'time': local, 'temp': temps[t]})
            first4 += 1
        #make sure the algorithm starts on the next day, not the current one
        if local in [0, 1, 2] and last_midnight == -1:
            last_midnight = t
        #finds the next midnight since the last one
        elif local in [0, 1, 2]:
            next_midnight = t
            high = temps[last_midnight]
            index = last_midnight
            #finds the highest temperature between two midnights and adds to the list of highs
            for p in range(last_midnight, next_midnight + 1):
                if temps[p] > high:
                    high = temps[p]
                    index = p

            highs.append(high)
            i_highs.append(index)
            #resets which index to start from
            last_midnight = next_midnight

    #finds the low temperatures between each high
    for i in range(1, len(highs)):
        low = temps[i_highs[i-1]]
        for j in range(i_highs[i-1], i_highs[i] + 1):
            if temps[j] < low:
                low = temps[j]

        lows.append(low)

    return {'highs': highs[:len(highs)-1], 'lows': lows, '12hr_forecast': forecast_12hr}


def clean_times(times, is_list=True):
    """Turns a list of strings formated in 'YYYY-MM-DD HH:MM:SS' to a list of
    datetime objects. Ignores the minutes and seconds of the string. Returns the
    new list."""
    if is_list == True:
        assert is_string_list(times)
    else:
        assert type(times) == str
        alt = times
        times = []
        times.append(alt)

    newtimes = []
    for i in times:
        year = int(i[:4])
        month = int(i[5:7])
        day = int(i[8:10])
        hour = int(i[11:13])

        time = datetime(year, month, day, hour)
        newtimes.append(time)

    return newtimes


def init_catwear():
    """Initializes the CatWear database."""
    print('Initializing CatWear database...')
    cats = [
        {'imagename': 'Bundle_Cat', 'ft_max': 25, 'ft_min': None, 'ct_max': to_celcius(25), 'ct_min': None},
        {'imagename': 'Jacket_Cat', 'ft_max': 32, 'ft_min': 25, 'ct_max': to_celcius(32), 'ct_min': to_celcius(25)},
        {'imagename': 'Sweater_Cat', 'ft_max': 50, 'ft_min': 32, 'ct_max': to_celcius(50), 'ct_min': to_celcius(32)},
        {'imagename': 'Hoodie_Cat', 'ft_max': 75, 'ft_min': 50, 'ct_max': to_celcius(75), 'ct_min': to_celcius(50)},
        {'imagename': 'T-Shirt_Cat', 'ft_max': 90, 'ft_min': 75, 'ct_max': to_celcius(90), 'ct_min': to_celcius(75)},
        {'imagename': 'Sweating_Cat', 'ft_max': None, 'ft_min': 90, 'ct_max': None, 'ct_min': to_celcius(90)}
    ]

    for c in cats:
        cat = CatWear(
            imagename = c['imagename'],
            ft_max = c['ft_max'],
            ft_min = c['ft_min'],
            ct_max = c['ct_max'],
            ct_min = c['ct_min'])
        db.session.add(cat)

    db.session.commit()
    print('CatWear initialized!')


def get_catwear(temp, units):
    """Determines the appropriate cat image for the given temperature in the
    given units.

    temp: number
    units: str, imperial or metric"""
    assert type(temp) in [int, float]
    assert type(units) == str and units in ['imperial', 'metric']
    try:
        if units == 'imperial':
            cat = CatWear.query.filter(CatWear.ft_min < temp, CatWear.ft_max >= temp).first()
        elif units == 'metric':
            cat = CatWear.query.filter(CatWear.ct_min < temp, CatWear.ct_max >= temp).first()
        return cat.serialize()

    except:
        return 'error'


def is_number_list(value):
    """Determines if the value passed in is a list of numbers and returns True if
    so and False otherwise.
    """
    if type(value) != list:
        return False

    for i in value:
        if type(i) not in [float, int]:
            return False

    return True


def is_string_list(times):
    """"Determines if the list passed is a list of strings, returns True if so,
    False otherwise.
    """
    if type(times) != list:
        return False

    for i in times:
        if type(i) != str:
            return False

    return True

def to_celcius(temp):
    """Converts a given temperature in fahrenheit to celcius.
    num: number"""
    assert type(temp) in [float, int]
    return (5/9)*(temp-32)
