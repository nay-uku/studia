import asyncio
import faust
import json
import datetime

from kafka import KafkaProducer
from profanityfilter import ProfanityFilter
from urlextract import URLExtract
from pymongo import MongoClient

# MONGO PT
MONGO_PT_IP = '10.7.38.68'
MONGO_PT_PORT = 27017
collection_name = 'faust_filter'

KAFKA_CLUSTER_IP = '10.7.38.66'
bootstrap_servers = [KAFKA_CLUSTER_IP + ":9092", KAFKA_CLUSTER_IP + ":9093", KAFKA_CLUSTER_IP + ":9094"]
kafka_producer = KafkaProducer(bootstrap_servers=bootstrap_servers,
                               value_serializer=lambda m: json.dumps(m, default=datetime_converter).encode('ascii'))


def datetime_converter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()


app = faust.App(
    'faust_filter',
    broker=[f'kafka://{KAFKA_CLUSTER_IP}:9092',
            f'kafka://{KAFKA_CLUSTER_IP}:9093',
            f'kafka://{KAFKA_CLUSTER_IP}:9094'],
    value_serializer="json"
)
raw_msgs_topic = app.topic('raw-msgs')


async def filter_language(msg):
    return msg.get('language') == 'en'


async def filter_profanity(msg):
    return ProfanityFilter().is_clean(msg.get('data'))


async def filter_source(msg):
    return msg.get('source') == 'twitter'


async def filter_url(msg):
    return not URLExtract().has_urls(msg.get('data'))


@app.agent(raw_msgs_topic)
async def filter_msg(msgs):
    async for msg in msgs:
        pt_data = {
            'msg': msg,
            'start_time': datetime.datetime.utcnow()
        }
        filter_values = await asyncio.gather(
            *[filter_language(msg), filter_profanity(msg), filter_source(msg), filter_url(msg)])
        is_valid = all(filter_values)
        topic = 'valid-msgs' if is_valid else 'invalid-msgs'
        kafka_producer.send(topic, value=msg)
        kafka_producer.flush()
        print(f'{datetime.datetime.utcnow()}: The message has been sent to the topic: "{topic}"')
        try:
            mongo_pt_client = MongoClient(MONGO_PT_IP, MONGO_PT_PORT)
            mongo_pt_db = mongo_pt_client["processing_time"]
            mongo_pt_col = mongo_pt_db[collection_name]
            pt_data['end_time'] = datetime.datetime.utcnow()
            mongo_pt_col.insert_one(pt_data)
        except Exception:
            print("Could not send processing time data to MongoDB!")
