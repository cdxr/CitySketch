# Filename: index.py
# Author: Craig Roche

import requests

from city_types import Location, LocalTime


##############################
### external API functions ###
##############################

# All external API calls should be confined to this module.
# These methods should only be called directly for testing and prototyping
# purposes.

# The city module provides a City class which encapsulates these methods, and
# should be considered the preferred means of obtaining this data.


# Note: All external API calls are done through the _make_request function,
#       which encapsulates calls to requests.get.
#
#       This is done so that we can change the exception handling behavior for
#       all external API calls by modifying the _make_request function.


"""
Make an HTTP get request with the given URL and parameters.
In the event of any exceptions related to the HTTP request, this function
catches the exception and returns None.
If 'print_errors' is True, the exceptions are printed.
"""
def _make_request(url, params, print_errors=True):
    try:
        response = requests.get(url, params=params).json()
    except requests.exceptions.RequestException as e:
        if print_errors:
            print "Exception making external API call"
            print e
        return None

    return response


# Note: _gmaps_lookup_city returns None for many different conditions.
#       We should probably create different exception types to represent
#       the different kinds of failure possible in this function.

"""
Use the Google Maps API to find the first city matching the given query.
Returns a dictionary on success, None on failure.
"""
def _gmaps_lookup_city(query):
    url = 'http://maps.googleapis.com/maps/api/geocode/json'
    params = {
        'address': query,
        'sensor': True,
    }

    try:
        response = requests.get(url, params=params).json()
    except requests.exceptions.RequestException as e:
        print "_gmaps_lookup_city(): ",  e
        return None

    response = _make_request(url, params)

    # the request failed
    if response is None:
        return None

    results = response['results']

    # no cities matched the query
    if not results:
        return None

    # restrict results to the first city
    city = None
    for i in range(0, 1): # change '1' to iterate for more results
        thisCity = results[i]
        address_types = thisCity['address_components'][0]['types']
        if address_types[0] == 'locality' or address_types[1] == 'political':
            city = thisCity

    # return the first result
    return city



"""
Use the OpenWeatherMap API to retrieve weather information for the given
Location.
Returns a dictionary on success, None on failure.
"""
def _lookup_weather(location):
    url = 'http://api.openweathermap.org/data/2.5/forecast/daily'
    params = {
        'lat': location.lat,
        'lon': location.lng,
        'cnt': 16,
        'units': 'imperial',
        'APPID': 'ef49a278b6557235d3372d9c5416d4f6'
    }

    return _make_request(url, params)


"""
Use the Wikipedia API to retrieve information for the given city.
Returns a dictionary on success, None on failure.
"""
def _lookup_wikipedia(city_name):
    url = 'https://en.wikipedia.org/w/api.php'
    params = {
        'action': 'opensearch',
        'search': city_name,
        'format': 'json'
    }

    return _make_request(url, params)


"""
Use the New York Times API to retrieve news information for the given city.
Returns a dictionary on success, None on failure.
"""
def _lookup_nyt(city_name):
    NYT_API_KEY = '532e9278d93c9c359096abdbbf5d65fd:14:74311752'

    url = 'http://api.nytimes.com/svc/search/v2/articlesearch.json'
    params = {
        'q': city_name,
        'sort': 'newest',
        'api-key': NYT_API_KEY,
    }

    return _make_request(url, params)


"""
Use the TimeZoneDB API to retrieve time information for the given Location.
Returns a LocalTime on success, None on failure.
"""
def _lookup_time(location):
    import time

    TIMEZONE_DB_KEY = 'RI1ZCW7725DU'

    url = 'http://api.timezonedb.com/'
    params = {
      'lat': location.lat,
      'lng': location.lng,
      'format': 'json',
      'key': TIMEZONE_DB_KEY,
    }

    response = _make_request(url, params=params)

    if response is None:
        return None

    # compute local time at given coordinates
    timestamp = float(response['timestamp'])
    local_time = time.gmtime(timestamp)

    return LocalTime(local_time, response['abbreviation'], response['zoneName'])
