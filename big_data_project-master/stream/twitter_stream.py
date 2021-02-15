#!/usr/bin/python3
import tweepy
import sys
import re
import json
import datetime
from langid.langid import LanguageIdentifier, model
from kafka import KafkaProducer
from pymongo import MongoClient

# MONGO PT
MONGO_PT_IP = '10.7.38.68'
MONGO_PT_PORT = 27017
collection_name = 'twitter_stream'

# Global variables
identifier = LanguageIdentifier.from_modelstring(model, norm_probs=True)

# KAFKA #
KAFKA_CLUSTER_IP = "10.7.38.66"
bootstrap_servers = [KAFKA_CLUSTER_IP + ":9092", KAFKA_CLUSTER_IP + ":9093", KAFKA_CLUSTER_IP + ":9094"]
kafka_producer = KafkaProducer(bootstrap_servers=bootstrap_servers,
                               value_serializer=lambda m: json.dumps(m, default=datetime_converter).encode('ascii'))


def datetime_converter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()


def twitter_auth():
    with open('twitter_auth.txt', 'r') as f:
        contents = [line.strip() for line in f if line.strip()]

    auth = tweepy.OAuthHandler(contents[0],
                               contents[1])
    auth.set_access_token(contents[2],
                          contents[3])
    api = tweepy.API(auth, wait_on_rate_limit=True)
    try:
        api.verify_credentials()
        print("Authentication OK")
    except:
        print("Error during authentication")
    return api


def get_language(msg):
    predictions = identifier.classify(msg)
    # Język rozpoznany z prawdopodobieństwem większym niż 80%
    if predictions[1] > 0.8:
        lang = predictions[0]
    else:
        lang = "Not recognized"
    return lang


# StreamListener class inherits from tweepy.StreamListener and overrides on_status/on_error methods.
class StreamListener(tweepy.StreamListener):
    def on_status(self, status):
        pt_data = {
            'msg': '',
            'start_time': datetime.datetime.utcnow()
        }
        # if "retweeted_status" attribute exists, flag this tweet as a retweet.
        is_retweet = hasattr(status, "retweeted_status")
        # check if text has been truncated
        if hasattr(status, "extended_tweet"):
            text = status.extended_tweet["full_text"]
        else:
            text = status.text
        text = (re.sub(r'<U+.*?>', '', text)).replace('\n', ' ').strip()
        lang = get_language(text)
        msg = {
            'author': status.user.screen_name,
            'location': status.user.location,
            'source': 'twitter',
            'timestamp': datetime.datetime.now(),
            'data': text,
            'language': lang
        }
        kafka_producer.send('raw-msgs', value=msg)
        kafka_producer.flush()
        print(msg)
        try:
            mongo_pt_client = MongoClient(MONGO_PT_IP, MONGO_PT_PORT)
            mongo_pt_db = mongo_pt_client["processing_time"]
            mongo_pt_col = mongo_pt_db[collection_name]
            pt_data['msg'] = msg
            pt_data['end_time'] = datetime.datetime.utcnow()
            mongo_pt_col.insert_one(pt_data)
        except Exception:
            print("Could not send processing time data to MongoDB!")

    def on_error(self, status_code):
        print("Encountered streaming error (", status_code, ")")
        sys.exit()


if __name__ == "__main__":
    api = twitter_auth()
    streamListener = StreamListener()
    stream = tweepy.Stream(auth=api.auth, listener=streamListener, tweet_mode='extended')
    tags = ["football", "cryptocurrencies", "coronavirus"]
    stream.filter(track=tags)
