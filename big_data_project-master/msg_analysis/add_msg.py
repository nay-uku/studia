#!/usr/bin/python3
import json
from kafka import KafkaConsumer
from model import *
from datetime import datetime
from pymongo import MongoClient

# MONGO PT
MONGO_PT_IP = '10.7.38.68'
MONGO_PT_PORT = 27017
collection_name = 'neo4j_msg_analysis'

KAFKA_CLUSTER_IP = "10.7.38.66"
bootstrap_servers = [KAFKA_CLUSTER_IP + ":9092", KAFKA_CLUSTER_IP + ":9093", KAFKA_CLUSTER_IP + ":9094"]
consumer = KafkaConsumer('raw-msgs', bootstrap_servers=bootstrap_servers,
                         value_deserializer=lambda m: json.loads(m.decode('ascii')))


def get_user(nick, service):
    user = User.nodes.first_or_none(nick=nick, service=service)
    if user is None:
        user = User(nick=nick, service=service).save()
    return user


def get_location(loc_name):
    loc_name = 'Unknown' if loc_name is None else loc_name
    location = Location.nodes.first_or_none(name=loc_name)
    if location is None:
        location = Location(name=loc_name).save()
    return location


def get_msg(text, language):
    msg = Message.nodes.first_or_none(text=text, language=language)
    if msg is None:
        msg = Message(text=text, language=language).save()
    return msg


for message in consumer:
    pt_data = {
        'msg': message,
        'start_time': datetime.utcnow()
    }
    user = get_user(message.value.get('author'), message.value.get('source'))
    location = get_location(message.value.get('location'))
    msg = get_msg(message.value.get('data'), message.value.get('language'))
    user.location.connect(location)
    user.messages.connect(msg, {'timestamp': datetime.strptime(message.value.get('timestamp'), '%Y-%m-%d %H:%M:%S.%f')})
    print(f'{datetime.utcnow()}: Message has been added.')
    try:
        mongo_pt_client = MongoClient(MONGO_PT_IP, MONGO_PT_PORT)
        mongo_pt_db = mongo_pt_client["processing_time"]
        mongo_pt_col = mongo_pt_db[collection_name]
        pt_data['end_time'] = datetime.utcnow()
        mongo_pt_col.insert_one(pt_data)
    except Exception:
        print("Could not send processing time data to MongoDB!")
