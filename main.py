from twikit import Client, TooManyRequests
import time
from datetime import datetime
import csv
from configparser import ConfigParser
from random import randint

MINIMUM_TWEETS = 10
QUERY = "Palestine OR Israel OR Gaza OR #IsraelPalestineConflict OR #Palestine OR #Gaza OR #Israel OR #IsraelGaza OR #IsraelGazaWar OR #Hamas"

# Login Credentials
config = ConfigParser()
config.read('config.ini')
username = config['X']['username']
email = config['X']['email']
password = config['X']['password']

# Autgenticate to X.com
#! 1) use the login credentials. 2) use cookies.
client = Client(language='en-US')
# client.login(auth_info_1=username, auth_info_2=email, password=password)
# client.save_cookies('cookies.json')

client.load_cookies('cookies.json')

# get tweets

tweets = client.search_tweet(QUERY,product='Top')

for tweet in tweets:
    print(vars(tweet))
    break