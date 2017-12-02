# coding: utf-8
import pickle
from pymongo import MongoClient

import sys
sys.path.append('../')
from classify_tweets import *

if __name__ == "__main__":
    client = MongoClient('localhost', 27017)
    db = client.taller04

    classifier = Classification()
    lang = 'es'

    # get tweets count
    tweets_count = db.tweets.count({"lang" : lang})
    print(tweets_count)
    page_size = 100
    total_page = int(tweets_count / page_size)
    if tweets_count % page_size > 0:
        total_page = total_page + 1

    for index in range(0, total_page):
        print(index)
        start = index * page_size

        # get tweets
        tweets = db.tweets.find({"lang" : lang}).skip(start).limit(page_size)
        # create dataset
        dataset = classifier.generate_dataset_by_lang(tweets, lang)
        # Classify tweets by polarity
        if lang == 'es':
            clf_polarities = classifier.classify_by_polarity(dataset)
        else:
            clf_polarities = classifier.classify_by_polarity_english(dataset)

        x = 0
        tweets.rewind()
        for tweet in tweets:
            polarity = classifier.get_polarity_by_lang(int(clf_polarities[x]), lang)
            nvars = {
                "polarity_id" : polarity[0],
                "polarity" : polarity[1],
            }
            db.tweets.update_one( {'_id' : tweet['_id']}, {'$set' : nvars} )
            x = x + 1
