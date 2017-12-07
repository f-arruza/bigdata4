# coding: utf-8
import json
from pymongo import MongoClient

if __name__ == "__main__":
    client = MongoClient('localhost', 27017)
    db = client.taller04

    # tweets = db.tweets.find({})
    #
    # fileJ = open('testfile2.json', 'w')
    #
    # for tweet in tweets:
    #     json_data = {
    #         'payload' : tweet['payload'].lower(),
    #         'account' : tweet['tweet']['user']['screen_name'],
    #         'collection' : 'tweets',
    #         'polarity_id' : tweet['polarity_id'],
    #         'polarity' : tweet['polarity'],
    #         'ref_id' : str(tweet['_id']),
    #     }
    #     json.dump(json_data, fileJ)
    #
    data = db.musicfans_topics.find({})
    fileJ = open('testfile.json', 'w')

    for topic in data:
        json_data = {
            'payload' : topic['title'].lower(),
            'account' : topic['author'],
            'collection' : 'musicfans_topics',
            'polarity_id' : 0,
            'polarity' : '',
            'ref_id' : str(topic['_id']),
        }
        json.dump(json_data, fileJ)

        json_data = {
            'payload' : topic['summary'].lower(),
            'account' : topic['author'],
            'collection' : 'musicfans_topics',
            'polarity_id' : 0,
            'polarity' : '',
            'ref_id' : str(topic['_id']),
        }
        json.dump(json_data, fileJ)

        for response in topic['responses']:
            json_data = {
                'payload' : response['title'].lower(),
                'account' : topic['author'],
                'collection' : 'musicfans_topics',
                'polarity_id' : 0,
                'polarity' : '',
                'ref_id' : str(topic['_id']),
            }
            json.dump(json_data, fileJ)

            json_data = {
                'payload' : response['summary'].lower(),
                'account' : topic['author'],
                'collection' : 'musicfans_topics',
                'polarity_id' : 0,
                'polarity' : '',
                'ref_id' : str(topic['_id']),
            }
            json.dump(json_data, fileJ)
        # print(json_data)
