from twikit import Client, TooManyRequests
import time
from datetime import datetime
import csv
from configparser import ConfigParser
from random import randint

MINIMUM_TWEETS = 4000
QUERY = "Palestine OR Israel OR Gaza OR #IsraelPalestineConflict OR #Palestine OR #Gaza OR #Israel OR #IsraelGaza OR #IsraelGazaWar OR #Hamas"

# Login Credentials
