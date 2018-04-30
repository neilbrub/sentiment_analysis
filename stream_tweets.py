import tweepy
import pandas as pd
import numpy as np
import json
import os

"""
Connect to Twitter using Tweepy API, stream tweets into csv file
"""


def authenticate():

	# Put auth info here (must first register app at https://apps.twitter.com/)
    CONSUMER_KEY = "SPZBOM4LkM8Fn6V6rmIs6LfVs"
    CONSUMER_SECRET = "Q2JYUvCNo4jq4T06K74ylPZmJfLue99wUkFI13caP8yAF13Fso"
    ACCESS_TOKEN = "910554867550294017-tNXbE3spX13Z6LIIMFWoszBxUwIaeQA"
    ACCESS_TOKEN_SECRET = "KGpQxUWgLMy0j0AkuC1IwhaC79Nq1uoXqwx6L3NmYLLyH"

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    
    return auth


class MyStreamListener(tweepy.StreamListener):
    
    def __init__(self):
    	self._tweets_streamed = 0

    def on_status(self, status):
        print(status.text)
    

    def on_data(self, raw_data):

	    try:
	        data = json.loads(raw_data)
	        print(data['text'], "\n")

	        if os.path.isfile('tweets.csv'):
	            newfile = False
	        else:
	            newfile = True
	            self._tweets_streamed = 0

	        with open('tweets.csv', 'a') as f:
	            if newfile:
		            f.write('tweets;;\n')
	            f.write(data['text'])
	            f.write(";;\n")
	            self._tweets_streamed += 1

	        # Stop stream automatically:
	        if self._tweets_streamed >= 20:
	        	print("20 tweets collected, stream terminating...")
	        	return False

	    except (KeyError, IOError): 
	        pass


    def on_error(self, status_code):
	    if status_code == 420:
	        return False


api = tweepy.API(authenticate())
listener = MyStreamListener()

topic = str(input("What topic would you like to know about?\n> "))

myStream = tweepy.Stream(auth = api.auth, listener = listener)
myStream.filter(track=[topic])
