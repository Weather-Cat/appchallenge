from db import db, User, CatWear
from datetime import datetime

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
    """Sorts out the highs and lows for a given block of temperatures. Returns a
    tuple, (highs, lows).

    temps: list of numbers
    times: list of dates/times in str format
    """
    #probably EXTREMELY buggy
    assert is_number_list(temps)
    assert is_string_list(times)

    times = clean_times(times)
    length = len(times)
    utc_now = datetime.now(timezone.utc)
    local_now = #datatime local_time
    offset = utc_now - local_now

    last_midnight = 0
    highs = []
    i_highs = []
    lows = []
    for t in range(last_midnight + 1, length + 1):
        local = times[t] - offset
        #make sure the algorithm starts on the next day, not the current one
        if local.seconds in [0, 3600, 7200] and last_midnight == 0:
            last_midnight = t

        #finds the next midnight since the last one
        elif local.seconds in [0, 3600, 7200]:
            next_midnight = t
            high = temps[last_midnight]
            #finds the highest temperature between two midnights and adds to the list of highs
            for p in range(last_midnight, next_midnight + 1):
                if temps[p] > high:
                    high = temp[p]
                    index = p

            highs.append(high)
            i_highs.append(index)
            #resets which index to start from
            last_midnight = next_midnight

    #finds the low temperatures between each high, BUGGY, this will error when i+1 doesn't exist
    for i in time_highs:
        low = temps[i]
        for j in range(i, i+1):
            if temps[j] < low:
                low = temps[j]

        lows.append(low)

    return (highs, lows)


def clean_times(times):
    """Turns a list of strings formated in 'YYYY-MM-DD HH:MM:SS' to a list of
    datetime objects. Ignores the minutes and seconds of the string. Returns the
    new list."""
    assert is_string_list(times)

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
    cats = [{'imagename': 'Bundle_Cat', 't_max': 20, 't_min': None},
        {'imagename': 'Jacket_Cat', 't_max': 35, 't_min': 20},
        {'imagename': 'Sweater_Cat', 't_max': 50, 't_min': 35},
        {'imagename': 'Hoodie_Cat', 't_max': 65, 't_min': 50},
        {'imagename': 'T-Shirt_Cat', 't_max': 80, 't_min': 65},
        {'imagename': 'Sweating_Cat', 't_max': None, 't_min': 80}
    ]

    for c in cats:
        cat = CatWear(imagename = c['imagename'], t_max = c['t_max'], t_min = c['t_min'])
        db.session.add(cat)

    db.session.commit()
    print('CatWear initialized!')


def get_catwear(temp):
    """Determines the appropriate cat image for the given temperature.
    temp: number"""
    assert type(temp) in [int, float]
    try:
        cat = Cat.query.filter_by(t_min < temp and t_max >= temp).first()
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
