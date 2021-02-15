import json
from kafka import KafkaConsumer


KAFKA_CLUSTER_IP = "10.7.38.66"
bootstrap_servers = [KAFKA_CLUSTER_IP + ":9092", KAFKA_CLUSTER_IP + ":9093", KAFKA_CLUSTER_IP + ":9094"]
consumer = KafkaConsumer('raw-msgs', bootstrap_servers=bootstrap_servers,
                         value_deserializer=lambda m: json.loads(m.decode('ascii')))

for message in consumer:
    print(message.value)
