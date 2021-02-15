import operator
import os
import string
import argparse
from config import MONGO_IP
from datetime import datetime
from datetime import timedelta
from pymongo import MongoClient

from graphs import *

# MONGO
mongo_client = MongoClient(MONGO_IP)
mongo_db = mongo_client["sentiment"]
mongo_col = mongo_db["sentiment"]

parser = argparse.ArgumentParser()
parser.add_argument("action", help="available: count")
parser.add_argument("-sd", "--startdate", help="start date - format %%Y%%m%%d (if left empty, data from today is returned")
parser.add_argument("-ed", "--enddate", help="end date - format %%Y%%m%%d (usable alongside start date only)")

args = parser.parse_args()

today = datetime.strptime(datetime.today().date().strftime("%Y-%m-%dT%H:%M:%S.000Z"), "%Y-%m-%dT%H:%M:%S.000Z")

if args.action == "count":
    if args.startdate:
        if args.enddate:
            start_date = datetime.strptime(datetime.strptime(args.startdate, "%Y%m%d").strftime("%Y-%m-%dT%H:%M:%S.000Z"), "%Y-%m-%dT%H:%M:%S.000Z")
            end_date = datetime.strptime((datetime.strptime(args.enddate, "%Y%m%d") + timedelta(days=1)).date().strftime("%Y-%m-%dT%H:%M:%S.000Z"), "%Y-%m-%dT%H:%M:%S.000Z")
            positive = mongo_col.find({"sentiment": "Positive", "timestamp": {"$gte": start_date, "$lte": end_date}}).count()
            negative = mongo_col.find({"sentiment": "Negative", "timestamp": {"$gte": start_date, "$lte": end_date}}).count()
            print(f"Positive tweets: {positive}\nNegative tweets: {negative}")
            bar_graph_save(['positive tweets', 'negative tweets'], [positive, negative],
                           f"Twitter sentiment analysis\n({start_date} - {end_date})")
        else:
            start_date = datetime.strptime(datetime.strptime(args.startdate, "%Y%m%d").strftime("%Y-%m-%dT%H:%M:%S.000Z"), "%Y-%m-%dT%H:%M:%S.000Z")
            positive = mongo_col.find(
                {"sentiment": "Positive", "timestamp": {"$gte": start_date}}).count()
            negative = mongo_col.find(
                {"sentiment": "Negative", "timestamp": {"$gte": start_date}}).count()
            print(f"Positive tweets: {positive}\nNegative tweets: {negative}")
            bar_graph_save(['positive tweets', 'negative tweets'], [positive, negative], f"Twitter sentiment analysis\n({start_date} - {today.strftime('%Y-%m-%d %H:%M:%S')})")
    else:
        positive = mongo_col.find(
            {"sentiment": "Positive", "timestamp": {"$gte": today}}).count()
        negative = mongo_col.find(
            {"sentiment": "Negative", "timestamp": {"$gte": today}}).count()
        print(f"Positive tweets: {positive}\nNegative tweets: {negative}")
        bar_graph_save(['positive tweets', 'negative tweets'], [positive, negative],
                       f"Twitter sentiment analysis today\n{today.strftime('%Y-%m-%d %H:%M:%S')}")