#!/usr/bin/python3
import json
import threading
from datetime import datetime
import socket
import os
from pymongo import MongoClient
from cassandra.cluster import Cluster
from kafka import KafkaConsumer

from config import KAFKA_CLUSTER_IP, KAFKA_BOOTSTRAP_SERVERS, CASSANDRA_IP

# MONGO PT
MONGO_PT_IP = '10.7.38.68'
MONGO_PT_PORT = 27017
collection_name = 'cassandra_statistics'

cass_cluster = Cluster([CASSANDRA_IP])
cass_session = cass_cluster.connect('statistics')

# mutex = threading.Lock()

class Thread(threading.Thread):
    def __init__(self, topic, group_id, brokers):
        threading.Thread.__init__(self)
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
                'timestamp': msg.value.get('timestamp'),
                'data': msg.value.get('data'),
                'language': msg.value.get('language'),
            }
            print(message['timestamp'])
            # custom_tokens = self.tokenizer.tokenize(message['data'])

            stmt = cass_session.prepare(
                    "INSERT INTO messages (author, location, source, time, msg_data, language, msg_day) VALUES (?,?,?,?,?,?,?)")
            qry = stmt.bind(
                [message['author'], message['location'], message['source'],
                 datetime.strptime(message['timestamp'], '%Y-%m-%d %H:%M:%S.%f'), message['data'], message['language'], message['timestamp'].split()[0].replace('-', '')])
            cass_session.execute(qry)

            try:
                mongo_pt_client = MongoClient(MONGO_PT_IP, MONGO_PT_PORT)
                mongo_pt_db = mongo_pt_client["processing_time"]
                mongo_pt_col = mongo_pt_db[collection_name]
                pt_data['end_time'] = datetime.utcnow()
                mongo_pt_col.insert_one(pt_data)
            except Exception:
                print("Could not send processing time data to MongoDB!")

            # mutex.acquire()
            # try:
            #     # Cassandra
            #     # stmt = cass_session.prepare(
            #     #     "INSERT INTO user_logs (log_day, topic, username, time, data) VALUES (?,?,?,?,?)")
            #     # qry = stmt.bind(
            #     #     [message.value['log_day'], message.topic, message.value['user'],
            #     #      datetime.strptime(message.value['time'], '%Y-%m-%d %H:%M:%S.%f'), message.value['msg']])
            #     # cass_session.execute(qry)
            #     pass
            # finally:
            #     mutex.release()


if __name__ == "__main__":
    # Utworzenie wątków - każdy wątek to osobny consumer

    thread1 = Thread('raw-msgs', 'cassandra-statistics', KAFKA_BOOTSTRAP_SERVERS)
    # thread2 = Thread('invalid-msgs', 'faust-filter', KAFKA_BOOTSTRAP_SERVERS)
    # Rozpoczęcie wątków
    thread1.start()
    # thread2.start()
    print("Wątek został uruchomiony")
