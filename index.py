# Filename: index.py
# Author: Adam Novotny
# Purpose: main routing file for third party API resources

import os
import requests
import random
from flask import Flask, render_template, request
from flask import redirect
from flask import jsonify, json

# custom imports
from city import City
from city_types import Location
import external
import valid_cities

# variables
app = Flask(__name__)

# show index.html
@app.route('/')
def show_index():
  return render_template('index.html')

# verify city using googleapis
@app.route('/gmaps-json', methods=['GET'])
def gmaps_json():
    city_query = request.args.get('city')
    city = City.lookup(city_query)

    if city is None:
        return jsonify({'gmaps-json': 'none'})
    else:
        return jsonify({'gmaps-json': city.to_json()})

# return weather json
@app.route('/weather-json', methods=['GET'])
def weather_json():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    location = Location(lat,lon)

    result = external._lookup_weather(location)
    return jsonify({'weather-json': result})

# return Wiki json
@app.route('/wiki-json', methods=['GET'])
def wiki_json():
    city_name = request.args.get('city')

    result = external._lookup_wikipedia(city_name)
    return jsonify({'wiki-json': result})

# return NYT json
@app.route('/nyt-json', methods=['GET'])
def nyt_json():
    city_name = request.args.get('city')

    result = external._lookup_nyt(city_name)
    return jsonify({'nyt-json': result})

# return current time json
@app.route('/time-json', methods=['GET'])
def time_json():
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    location = Location(lat,lng)
    
    local_time = external._lookup_time(location)

    return jsonify({
        'time':      local_time.as_string(),
        'zone_abbr': local_time.zone_abbr,
        'zone_name': local_time.zone_name,
    })


# verify city using googleapis
@app.route('/random-city')
def random_city():
  return jsonify({'random-city': random.choice(valid_cities.cityList)})



if __name__ == '__main__':
  app.debug = True # used for dev only
  host = '0.0.0.0'
  app.run(host)
