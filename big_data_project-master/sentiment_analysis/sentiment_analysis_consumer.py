#!/usr/bin/python3
import json
import threading
from datetime import datetime
import pickle
import os
import schedule

from pymongo import MongoClient

from nltk.tokenize import TweetTokenizer

from kafka import KafkaConsumer

from config import MODEL_PICKLE_FILENAME, KAFKA_CLUSTER_IP, KAFKA_BOOTSTRAP_SERVERS, MONGO_IP

from sentiment_analysis import create_model

def update_model():
    print(f"Aktualizuję model")
    create_model()
    try:
        f = open(MODEL_PICKLE_FILENAME, 'rb')
        classifier = pickle.load(f)
        f.close()
    except Exception as e:
        print(f"Wystąpił błąd podczas aktualizowania modelu: {e}")
        return None
    return classifier

def get_model():
    if not os.path.isfile(MODEL_PICKLE_FILENAME):
        create_model()
    try:
        f = open(MODEL_PICKLE_FILENAME, 'rb')
        classifier = pickle.load(f)
        f.close()
    except Exception as e:
        print(f"Wystąpił błąd podczas ładowania modelu: {e}")
        return None
    return classifier

# MONGO
mongo_client = MongoClient(MONGO_IP)
mongo_db = mongo_client["sentiment"]
mongo_col = mongo_db["sentiment"]

# MONGO PT
MONGO_PT_IP = '10.7.38.68'
MONGO_PT_PORT = 27017
collection_name = 'mongo_sentiment_analysis'

schedule.every(1).minutes.do(update_model)

class Thread(threading.Thread):
    def __init__(self, topic, group_id, brokers):
        threading.Thread.__init__(self)

        self.classifier = get_model()
        self.tokenizer = TweetTokenizer()

        # Utworzenie consumer-a do odczytywania danych z topic-u registration-logs
        self.consumer = KafkaConsumer(topic, group_id=group_id, bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
                                      value_deserializer=lambda m: json.loads(m.decode('ascii')))


    def run(self):
        for msg in self.consumer:
            pt_data = {
                'msg': msg,
                'start_time': datetime.utcnow()
            }

            message = {
                'author': msg.value.get('author'),
                'location': msg.value.get('location'),
                'source': msg.value.get('source'),
                'timestamp': datetime.strptime(datetime.strptime(msg.value.get('timestamp'), '%Y-%m-%d %H:%M:%S.%f').strftime("%Y-%m-%dT%H:%M:%S.000Z"), "%Y-%m-%dT%H:%M:%S.000Z"),
                'data': msg.value.get('data'),
                'language': msg.value.get('language'),
            }


            custom_tokens = self.tokenizer.tokenize(message['data'])
            prob_dict = self.classifier.prob_classify(dict([token, True] for token in custom_tokens))

            if prob_dict.prob('Negative') < 0.15:
                category = 'Positive'
            elif prob_dict.prob('Negative') > 0.85:
                category = 'Negative'
            else:
                category = "Inconclusive"

            # print(f"The message:\n{message['data']}\nwas assigned the following category:\n{category}\n")

            message["sentiment"] = category

            if category != "Inconclusive":
                mongo_col.insert_one(message)

            try:
                mongo_pt_client = MongoClient(MONGO_PT_IP, MONGO_PT_PORT)
                mongo_pt_db = mongo_pt_client["processing_time"]
                mongo_pt_col = mongo_pt_db[collection_name]
                pt_data['end_time'] = datetime.utcnow()
                mongo_pt_col.insert_one(pt_data)
            except Exception:
                pass

            schedule.run_pending()


if __name__ == "__main__":
    # Utworzenie wątków - każdy wątek to osobny consumer

    thread1 = Thread('valid-msgs', 'mongo_sentiment_analysis', KAFKA_BOOTSTRAP_SERVERS)
    # Rozpoczęcie wątków
    thread1.start()
    print("Wątek został uruchomiony")
