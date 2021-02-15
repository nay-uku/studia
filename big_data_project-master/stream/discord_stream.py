#!/usr/bin/python3
import datetime
import discord
import json
from kafka import KafkaProducer
from langid.langid import LanguageIdentifier, model
from pymongo import MongoClient

# MONGO PT
MONGO_PT_IP = '10.7.38.68'
MONGO_PT_PORT = 27017
collection_name = 'discord_stream'

# Global variables
identifier = LanguageIdentifier.from_modelstring(model, norm_probs=True)

# DISCORD #
client = discord.Client()

# KAFKA #
KAFKA_CLUSTER_IP = "10.7.38.66"
bootstrap_servers = [KAFKA_CLUSTER_IP + ":9092", KAFKA_CLUSTER_IP + ":9093", KAFKA_CLUSTER_IP + ":9094"]
kafka_producer = KafkaProducer(bootstrap_servers=bootstrap_servers,
                               value_serializer=lambda m: json.dumps(m, default=datetime_converter).encode('ascii'))


def datetime_converter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()


def get_language(msg):
    predictions = identifier.classify(msg)
    # Język rozpoznany z prawdopodobieństwem większym niż 80%
    if predictions[1] > 0.8:
        lang = predictions[0]
    else:
        lang = "Not recognized"
    return lang


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.channel.name == 'channel_stream':
        pt_data = {
            'msg': '',
            'start_time': datetime.datetime.utcnow()
        }
        text = message.content
        lang = get_language(text)
        msg = {
            'author': message.author.name,
            'location': None,
            'source': 'discord',
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

with open('discord_auth.txt', 'r') as f:
    token = f.readline().strip()
    client.run(token)
