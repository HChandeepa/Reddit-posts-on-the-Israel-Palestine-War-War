from twikit import Client, TooManyRequests
import time
from datetime import datetime
import csv
from configparser import ConfigParser
from random import randint
import asyncio

# Set minimum tweets to collect (adjust based on your requirement)
MINIMUM_TWEETS = 5000  # You want 4000-5000 tweets

# Define query for the Palestine-Israel conflict
QUERY = '''
(Palestine OR Israel OR Gaza OR #IsraelPalestineConflict OR #Palestine OR #Gaza OR #Israel 
OR #IsraelGaza OR #IsraelGazaWar OR #Hamas) 
lang:en until:2024-10-07 since:2023-10-07
'''

# Function to fetch tweets
async def get_tweets(tweets):
    if tweets is None:
        # Get the first batch of tweets
        print(f'{datetime.now()} - Getting tweets...')
        tweets = await client.search_tweet(QUERY, product='Top')  # Use "Top" or "Latest"
    else:
        wait_time = randint(5, 10)
        print(f'{datetime.now()} - Getting next tweets after {wait_time} seconds ...')
        await asyncio.sleep(wait_time)
        tweets = await tweets.next()  # Get the next page of tweets

    return tweets

# Load credentials from a config file
config = ConfigParser()
config.read('config.ini')
username = config['X']['username']
email = config['X']['email']
password = config['X']['password']

# Create a CSV file to store the data
with open('palestine_israel_tweets.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Columns for your coursework
    writer.writerow([
        'Tweet_count', 'Username', 'Text', 'Created At', 
        'Retweets', 'Likes'
    ])

# Authenticate to X.com (Twitter alternative)
client = Client(language='en-US')

# Load previously saved cookies
client.load_cookies('cookies.json')

# Initialize variables
tweet_count = 0
tweets = None

# Define the main async function to fetch tweets
async def main():
    global tweet_count, tweets

    # Loop to fetch tweets until the desired number is reached
    while tweet_count < MINIMUM_TWEETS:
        try:
            tweets = await get_tweets(tweets)
        except TooManyRequests as e:
            rate_limit_reset = datetime.fromtimestamp(e.rate_limit_reset)
            print(f'{datetime.now()} - Rate limit reached. Waiting until {rate_limit_reset}')
            wait_time = rate_limit_reset - datetime.now()
            await asyncio.sleep(wait_time.total_seconds())
            continue

        if not tweets:
            print(f'{datetime.now()} - No more tweets found')
            break

        # Process tweets
        for tweet in tweets:
            tweet_count += 1
            # Extract tweet data
            tweet_data = [
                tweet_count, tweet.user.name, tweet.text, 
                tweet.created_at, tweet.retweet_count, tweet.favorite_count
            ]

            # Write data to the CSV file
            with open('palestine_israel_tweets.csv', 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(tweet_data)

        print(f'{datetime.now()} - Got {tweet_count} tweets')

    print(f'{datetime.now()} - Done! Collected {tweet_count} tweets.')

# Run the main function
asyncio.run(main())
