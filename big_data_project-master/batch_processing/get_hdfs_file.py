from hdfs import *
import pickle

client = InsecureClient('http://10.7.38.69:9870', user='root')
print(client.list("input"))
# client.download("input/sentiment_analysis.pickle","") # download from hdfs
# open and process in hdfs
with client.read("input/sentiment_analysis.pickle") as reader:
    content = reader.read()
