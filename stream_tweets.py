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
    CONSUMER_KEY = ""
    CONSUMER_SECRET = ""
    ACCESS_TOKEN = ""
    ACCESS_TOKEN_SECRET = ""

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    
    return auth


class MyStreamListener(tweepy.StreamListener):
    

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
	            
	        with open('tweets.csv', 'a') as f:
	            if newfile:
	                f.write('tweets;;\n')
	            f.write(data['text'])
	            f.write(";;\n")
	        f.close()

		except KeyError, IOError: 
	    	pass


   	def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_data disconnects the stream
            return False


api = tweepy.API(authenticate())
listener = MyStreamListener()

topic = str(input("What topic would you like to know about?"))

myStream = tweepy.Stream(auth = api.auth, listener = listener)
myStream.filter(track=[topic])
