# coding: utf-8
import json
from pymongo import MongoClient

if __name__ == "__main__":
    client = MongoClient('localhost', 27017)
    db = client.taller04

    tweets = db.tweets.find({}).skip(250001).limit(250000)

    fileJ = open('testfile2.json', 'w')

    for tweet in tweets:
        json_data = {
            'payload' : tweet['payload'].lower(),
            'account' : tweet['tweet']['user']['screen_name'],
            'collection' : 'tweets',
            'polarity_id' : tweet['polarity_id'],
            'polarity' : tweet['polarity'],
            'ref_id' : str(tweet['_id']),
        }
        json.dump(json_data, fileJ)
        # print(json_data)
