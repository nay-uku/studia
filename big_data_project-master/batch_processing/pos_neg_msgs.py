import csv
from textblob import TextBlob
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
from pylab import rcParams

rcParams['figure.figsize'] = 12, 8


def cleanUpTweet(txt):
    # Remove mentions
    txt = re.sub(r'@[A-Za-z0-9_]+', '', txt)
    # Remove hashtags
    txt = re.sub(r'#', '', txt)
    # Remove retweets:
    txt = re.sub(r'RT : ', '', txt)
    # Remove urls
    txt = re.sub(r'https?:\/\/[A-Za-z0-9\.\/]+', '', txt)
    return txt


def getTextPolarity(txt):
    return TextBlob(txt).sentiment.polarity


tweets = []
with open('twitter_data.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        tweets.append(row[0])

df = pd.DataFrame(data=[tweet for tweet in tweets], columns=['Tweet'])
df['Tweet'] = df['Tweet'].apply(cleanUpTweet)
df['Polarity'] = df['Tweet'].apply(getTextPolarity)
df = df.drop(df[df['Tweet'] == ''].index)
with open('pos_tweet.csv', 'w') as f_pos:
    with open('neg_tweet.csv', 'w') as f_neg:
        writer_pos = csv.writer(f_pos)
        writer_neg = csv.writer(f_neg)
        for i in df.index:
            if df['Polarity'][i] > 0:
                writer_pos.writerow([df['Tweet'][i]])
            if df['Polarity'][i] < 0:
                writer_neg.writerow([df['Tweet'][i]])
