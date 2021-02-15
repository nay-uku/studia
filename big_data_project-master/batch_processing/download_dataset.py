import random

import tweepy
import csv


def twitter_auth():
    with open('./../twitter_auth.txt', 'r') as f:
        contents = [line.strip() for line in f if line.strip()]
    auth = tweepy.OAuthHandler(contents[0], contents[1])
    auth.set_access_token(contents[2], contents[3])
    api = tweepy.API(auth, wait_on_rate_limit=True)
    try:
        api.verify_credentials()
        print("Authentication OK")
    except:
        print("Error during authentication")
    return api


def download_tweets(api):
    filename = 'twitter_data.csv'
    date_since = "2020-11-01"

    n = 10000
    football = tweepy.Cursor(api.search, q='football', lang='en', since=date_since).items(n)
    crypto = tweepy.Cursor(api.search, q='cryptocurrencies', lang='en', since=date_since).items(n)
    corona = tweepy.Cursor(api.search, q='coronavirus', lang='en', since=date_since).items(n)

    football_list = [[tweet.text, "football"] for tweet in football]
    crypto_list = [[tweet.text, "cryptocurrencies"] for tweet in crypto]
    corona_list = [[tweet.text, "coronavirus"] for tweet in corona]
    all_list = football_list + crypto_list + corona_list
    random.shuffle(all_list)

    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(all_list)


api = twitter_auth()
download_tweets(api)
