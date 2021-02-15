import json
import threading
from datetime import datetime
import socket

from cassandra.cluster import Cluster
from kafka import KafkaConsumer

# CLUSTER_IP = "localhost"
CLUSTER_IP = "192.168.1.233"

# CASSANDRA #
cass_cluster = Cluster([CLUSTER_IP])
cass_session = cass_cluster.connect('cassandra_nosql')


class Thread(threading.Thread):
    def __init__(self, topic, group_id, broker):
        threading.Thread.__init__(self)
        # Utworzenie consumer-a do odczytywania danych z topic-u registration-logs
        self.consumer = KafkaConsumer(topic, group_id=group_id, bootstrap_servers=[broker],
                                      value_deserializer=lambda m: json.loads(m.decode('ascii')))

    def run(self):
        for message in self.consumer:
            # Log po sockecie tcp na port 5000 do logstasha, który wkłada go do elastica
            HOST, PORT = CLUSTER_IP, 5000
            m = {"index": message.topic, "type": "log", "user": message.value['user'], "msg": message.value['msg']}
            data = json.dumps(m)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                sock.connect((HOST, PORT))
                sock.sendall(bytes(data, encoding="utf-8"))
            finally:
                sock.close()
            # print("Sent:     {}".format(data))
            # Cassandra
            stmt = cass_session.prepare(
                "INSERT INTO user_logs (log_day, topic, username, time, data) VALUES (?,?,?,?,?)")
            qry = stmt.bind(
                [message.value['log_day'], message.topic, message.value['user'],
                 datetime.strptime(message.value['time'], '%Y-%m-%d %H:%M:%S.%f'), message.value['msg']])
            cass_session.execute(qry)
            print("Log saved in Cassandra. Topic: " + message.topic + " , Value: { 'user': '" + message.value['user'] +
                  "', 'time': '" + message.value['time'] +
                  "', 'msg': '" + message.value['msg'] + "' }")


# Utworzenie wątków - każdy wątek to osobny consumer
thread1 = Thread('login-logs', "test-consumer-group", CLUSTER_IP + ":9092")
thread2 = Thread('registration-logs', "test-consumer-group", CLUSTER_IP + ":9092")
thread3 = Thread('send-message-logs', "test-consumer-group", CLUSTER_IP + ":9092")

# Rozpoczęcie wątków
thread1.start()
thread2.start()
thread3.start()
print("Wątki zostały uruchomione")
