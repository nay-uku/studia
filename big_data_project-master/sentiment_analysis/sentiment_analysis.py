import random
import pickle
import json
import hdfs

from config import MODEL_PICKLE_FILENAME

client = hdfs.InsecureClient('http://10.7.38.69:9870', user='root')
import nltk
# from nltk.corpus import twitter_samples
from nltk.stem import WordNetLemmatizer
from nltk.tag import pos_tag
from nltk.corpus import stopwords
from nltk import NaiveBayesClassifier

def clean_data(token):
    return [item for item in token if not item.startswith("http") and not item.startswith("@")]

def lemmatization(token):
    lemmatizer = WordNetLemmatizer()

    result = []
    for token, tag in pos_tag(token):
        tag = tag[0].lower()
        token = token.lower()
        if tag in "nva":
            result.append(lemmatizer.lemmatize(token, pos=tag))
        else:
            result.append(lemmatizer.lemmatize(token))
    return result

def remove_stop_words(token, stop_words):
    return [item for item in token if item not in stop_words]

def transform(token):
    result = {}
    for item in token:
        result[item] = True
    return result

def create_model():
    nltk.download('stopwords')
    nltk.download('averaged_perceptron_tagger')
    # nltk.download('twitter_samples')
    nltk.download('wordnet')

    # KB

    # Step 1: Gather data
    with client.read('input/twitter_samples/positive_tweets.json', encoding='utf-8') as reader:
        positive_tweets_hdfs = [json.loads(line) for line in reader]
    with client.read('input/twitter_samples/negative_tweets.json', encoding='utf-8') as reader:
        negative_tweets_hdfs = [json.loads(line) for line in reader]

    positive_tweets_tokens = [tweet["text"].split() for tweet in positive_tweets_hdfs]
    negative_tweets_tokens = [tweet["text"].split() for tweet in negative_tweets_hdfs]

    # Step 2: Clean, Lemmatize, and remove Stop Words
    stop_words = stopwords.words('english')
    positive_tweets_tokens_cleaned = [remove_stop_words(lemmatization(clean_data(token)), stop_words) for token in
                                      positive_tweets_tokens]
    negative_tweets_tokens_cleaned = [remove_stop_words(lemmatization(clean_data(token)), stop_words) for token in
                                      negative_tweets_tokens]
    # Step 3: Transform data
    positive_tweets_tokens_transformed = [(transform(token), "Positive") for token in positive_tweets_tokens_cleaned]
    negative_tweets_tokens_transformed = [(transform(token), "Negative") for token in negative_tweets_tokens_cleaned]

    # Step 4: Create data set
    dataset = positive_tweets_tokens_transformed + negative_tweets_tokens_transformed
    random.shuffle(dataset)

    train_data = dataset[:7000]
    # test_data = dataset[7000:]

    # Step 5: Train data
    classifier = NaiveBayesClassifier.train(train_data)

    # Step 7: Save the pickle
    f = open(MODEL_PICKLE_FILENAME, 'wb')
    pickle.dump(classifier, f)
    f.close()
