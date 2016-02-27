import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir)
import oauth2

import email_support
import external
import valid_cities
from sensitive_text import sensitive_text

def test_gmaps(city):
    return external._gmaps_lookup_city(city)

def test_autocomplete():
    return valid_cities.autocomplete_list()


def test_twitter(city):
    url = 'https://api.twitter.com/1.1/search/tweets.json?q=paris'
    key = '4898127648-hImwrcGlSCMqYvKIFl5BCZXAZAWunJ7FAtsrHYO'
    secret = 'BcvtY6dYTlzFboKjQXtfaQYGHNZrZSJebzA3FzQVdXSiq'
    return external._lookup_twitter(city)

def oauth_req():
    CONSUMER_KEY = 'I9CBjfoBWNLZTF71hCzo1j9XT'
    CONSUMER_SECRET = 'GGmjnZRHHUD52AdeGVD5qPr5CxibJbn6Xiq7JONi1ydzTREuCh'
    consumer = oauth2.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
    token = oauth2.Token(key=key, secret=secret)
    client = oauth2.Client(consumer, token)
    resp, content = client.request( url, method=http_method, body=post_body, headers=http_headers )
    return content
    
    home_timeline = oauth_req( 'https://api.twitter.com/1.1/statuses/home_timeline.json', 'abcdefg', 'hijklmnop' )


def test_sensitive_text():
    input_text = 'Beautiful, is; better*than\nugly#car#bus1'
    assert(sensitive_text(input_text) == False) # "test_sensitive_text test 1"
    input_text = 'Beautiful, is; better*than\sex#car#bus2'
    assert(sensitive_text(input_text) == True) # "test_sensitive_text test 2"
    input_text = 'Beautiful, is; better*than.ass#car#bus3'
    assert(sensitive_text(input_text) == True) # "test_sensitive_text test 3"
    input_text = 'Beautiful, is; better*than.any#ass#bus4'
    assert(sensitive_text(input_text) == True) # "test_sensitive_text test 4"
    input_text = 'Beautiful, is; better*than.any# ass#bus5'
    assert(sensitive_text(input_text) == True) # "test_sensitive_text test 5"
    input_text = 'Beautiful, is; better*than.any#   ass #bus6'
    assert(sensitive_text(input_text) == True) # "test_sensitive_text test 6"
    input_text = 'Beautiful, is; ?ass?better*than.any#   ok #bus7'
    assert(sensitive_text(input_text) == True) # "test_sensitive_text test 7"
    input_text = 'Beautiful, is; @ass?better*than.any#   ok #bus8'
    assert(sensitive_text(input_text) == True) # "test_sensitive_text test 8"
    input_text = '#  #'
    assert(sensitive_text(input_text) == False) # "test_sensitive_text test 9"

def test_email_support():
    # to do using get
    pass

if __name__ == "__main__":
    #print(test_gmaps("Mexico City"))
    #print(test_autocomplete())
    #print(test_twitter("paris"))
    test_sensitive_text()
    test_email_support()
    
