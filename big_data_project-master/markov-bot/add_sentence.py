#!/usr/bin/python3
import json
from kafka import KafkaConsumer
from model import *
from nltk.tokenize import TweetTokenizer
from datetime import datetime
from pymongo import MongoClient

# MONGO PT
MONGO_PT_IP = '10.7.38.68'
MONGO_PT_PORT = 27017
collection_name = 'neo4j_markov_bot'

def get_word(word_name):
    word = Word.nodes.first_or_none(name=word_name)
    if word is None:
        word = Word(name=word_name).save()
    return word


def add_sentence(sentence):
    token_list = TweetTokenizer().tokenize(sentence)
    for i in range(1, len(token_list)):
        prev_word = get_word(token_list[i - 1])
        curr_word = get_word(token_list[i])
        prev_word.next_words.connect(curr_word)
    print(f'{datetime.utcnow()}: Sentence has been added.')


KAFKA_CLUSTER_IP = "10.7.38.66"
bootstrap_servers = [KAFKA_CLUSTER_IP + ":9092", KAFKA_CLUSTER_IP + ":9093", KAFKA_CLUSTER_IP + ":9094"]
consumer = KafkaConsumer('valid-msgs', bootstrap_servers=bootstrap_servers,
                         value_deserializer=lambda m: json.loads(m.decode('ascii')))

for message in consumer:
    pt_data = {
        'msg': message,
        'start_time': datetime.utcnow()
    }
    add_sentence(message.value.get('data'))
    try:
        mongo_pt_client = MongoClient(MONGO_PT_IP, MONGO_PT_PORT)
        mongo_pt_db = mongo_pt_client["processing_time"]
        mongo_pt_col = mongo_pt_db[collection_name]
        pt_data['end_time'] = datetime.utcnow()
        mongo_pt_col.insert_one(pt_data)
    except Exception:
        print("Could not send processing time data to MongoDB!")
