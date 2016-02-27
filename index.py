# Filename: index.py
# Author: Adam Novotny
# Purpose: main routing file for third party API resources

import os
import requests
import random
from flask import Flask, render_template, url_for, request
from flask import redirect, flash
from flask import jsonify, json

# custom imports
from city import City
from city_types import Location
import external
import valid_cities
import city_desc
import email_support
import setup

# variables
app = Flask(__name__)
setup.setup_env(app)

# show index.html
@app.route('/')
def show_index():
  return render_template('index.html')


# handle contact form
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'GET':
        return render_template('contact.html')
    else:
        name = request.form['name']
        sender = request.form['email-address']
        text_body = 'Message from: ' + name + "\n" + request.form['message']
        subject = 'Email from ' + name
        recipients = ['citysketch@outlook.com']
        try:
          response = email_support.send_email(app, subject, sender, recipients, text_body)
          flash('Thank you for your message.')
          return redirect(url_for('show_index'))
        except:
          flash('Invalid inputs. Please use a valid email address.')
          return redirect(url_for('contact'))


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
  return jsonify({'random-city': random.choice(valid_cities.tested_list)})


# verify city using googleapis
@app.route('/autocomplete')
def autocomplete():
  return json.dumps(valid_cities.autocomplete_list())


# return city description json
@app.route('/city-description', methods=['GET'])
def city_description():
    city = request.args.get('city')
    response = city_desc._get(city)
    return json.dumps(response)


# return twitter json
@app.route('/twitter-json', methods=['GET'])
def twitter_json():
    city = request.args.get('city')
    result = external._lookup_twitter(city)
    return jsonify({'twitter-json': result})


# return true if city input was tested
@app.route('/tested-city', methods=['GET'])
def tested_city():
    city = request.args.get('city')
    if city in valid_cities.tested_list:
        return jsonify({'response': 'true'})
    else:
        return jsonify({'response': 'false'})


# return true if city input was tested
@app.route('/submit-message', methods=['POST'])
def submit_message():
    print(request.form['name'])
    subject = 'Test flask email'
    sender = 'test@outlook.com'
    recipients = ['citysketch@outlook.com']
    text_body = 'Test text from flask app'
    response = email_support.send_email(subject, sender, recipients, text_body)
    return render_template('index.html')

if __name__ == '__main__':
  app.debug = True # used for dev only
  host = '0.0.0.0'
  app.run(host)
