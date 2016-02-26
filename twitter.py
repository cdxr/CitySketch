# Filename: twitter.py
# Author: Craig Roche, Adam Novotny

import oauth2
import json
import valid_cities
from sensitive_text import sensitive_text

"""
Use twitter API and oauth2 authetication to obtain twitter search results
"""
def get_twitter(city):
    if city not in valid_cities.twitter_ban: #city in valid_cities.tested_list:
        query = city
        count = '100'
        url = 'https://api.twitter.com/1.1/search/tweets.json?q=%23' + query + '&count=' + count
        key = '4898127648-hImwrcGlSCMqYvKIFl5BCZXAZAWunJ7FAtsrHYO'
        secret = 'BcvtY6dYTlzFboKjQXtfaQYGHNZrZSJebzA3FzQVdXSiq'
        return oauth_req(url, key, secret)
    else:
        return ['twitter_not_allowed']

# authenticate and obtain contents
def oauth_req(url, key, secret, http_method="GET", post_body="", http_headers=None):
    CONSUMER_KEY = 'I9CBjfoBWNLZTF71hCzo1j9XT'
    CONSUMER_SECRET = 'GGmjnZRHHUD52AdeGVD5qPr5CxibJbn6Xiq7JONi1ydzTREuCh'
    consumer = oauth2.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
    token = oauth2.Token(key=key, secret=secret)
    client = oauth2.Client(consumer, token)
    resp, content = client.request( url, method=http_method, body=post_body, headers=http_headers )
    parsed_twitter = parse_twitter(json.loads(content))
    return parsed_twitter
    #return json.loads(content) #returns full json content

# parse contents for required results only
def parse_twitter(raw):
    MAX_TWEETS = 30
    count = 0
    response = []
    for tweet in raw['statuses']:
        try:
            # only return <30 english tweets with no sensitive content 
            if (tweet['lang'] == 'en') and \
               count < MAX_TWEETS and tweet['possibly_sensitive'] == False:
                count += 1
                selection = []
                selection.append({'date': tweet['created_at']})
                text = tweet['text']
                if sensitive_text(text) == True:
                    # sensitive word -> exclude
                    continue
                else:
                    selection.append({'text': text})
                hashtags = []
                for tag in tweet['entities']['hashtags']:
                    hashtags.append(tag['text'])
                selection.append({'hashtags': hashtags})
                try:
                    image_url = tweet['entities']['media'][0]['media_url']
                    selection.append({'image_url': image_url})
                except:
                    pass # no image
                response.append(selection)
        except:
            pass #possible sensitive content
    return response

