import argparse
from datetime import datetime
from datetime import timedelta
from pymongo import MongoClient
from statistics import mean

# MONGO PT
MONGO_PT_IP = '10.7.38.68'
MONGO_PT_PORT = 27017
collections = ['cassandra_statistics', 'discord_stream', 'faust_filter', 'mongo_sentiment_analysis', 'neo4j_markov_bot', 'neo4j_msg_analysis', 'twitter_stream']

parser = argparse.ArgumentParser()
parser.add_argument("collection_name", help=f"available: {collections}")
parser.add_argument("-sd", "--startdate", help="start date - format %%Y%%m%%d (if left empty, data from today is returned")
parser.add_argument("-ed", "--enddate", help="end date - format %%Y%%m%%d (usable alongside start date only)")

args = parser.parse_args()
today = datetime.strptime(datetime.today().date().strftime("%Y-%m-%dT%H:%M:%S.000Z"), "%Y-%m-%dT%H:%M:%S.000Z")

collection_name = args.collection_name
if collection_name not in collections:
    print('Invalid collection_name')
else:
    mongo_pt_client = MongoClient(MONGO_PT_IP, MONGO_PT_PORT)
    mongo_pt_db = mongo_pt_client["processing_time"]
    mongo_pt_col = mongo_pt_db[collection_name]
    if args.startdate:
        if args.enddate:
            start_date = datetime.strptime(datetime.strptime(args.startdate, "%Y%m%d").strftime("%Y-%m-%dT%H:%M:%S.000Z"), "%Y-%m-%dT%H:%M:%S.000Z")
            end_date = datetime.strptime((datetime.strptime(args.enddate, "%Y%m%d") + timedelta(days=1)).date().strftime("%Y-%m-%dT%H:%M:%S.000Z"), "%Y-%m-%dT%H:%M:%S.000Z")
            processing_times = []
            for info in mongo_pt_col.find({"start_time": {"$gte": start_date, "$lte": end_date}}):
                processing_times.append((info["end_time"] - info["start_time"]).total_seconds())
            if len(processing_times) > 0:
                print(f"Mean processing time: {mean(processing_times)}s")
            else:
                print("No data found")
        else:
            start_date = datetime.strptime(datetime.strptime(args.startdate, "%Y%m%d").strftime("%Y-%m-%dT%H:%M:%S.000Z"), "%Y-%m-%dT%H:%M:%S.000Z")
            processing_times = []
            for info in mongo_pt_col.find({"start_time": {"$gte": start_date}}):
                processing_times.append((info["end_time"] - info["start_time"]).total_seconds())
            if len(processing_times) > 0:
                print(f"Mean processing time: {mean(processing_times)}s")
            else:
                print("No data found")
    else:
        processing_times = []
        for info in mongo_pt_col.find({"start_time": {"$gte": today}}):
            processing_times.append((info["end_time"] - info["start_time"]).total_seconds())
        if len(processing_times) > 0:
            print(f"Mean processing time: {mean(processing_times)}s")
        else:
            print("No data found")
