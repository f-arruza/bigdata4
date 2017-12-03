# coding: utf-8
import os
import json
import requests
from bson.objectid import ObjectId
from pymongo import MongoClient

def extract_entities(token, text):
    payload = 'key='+ token +'&lang=en&txt=' + text + '&tt=a'
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.request("POST", url, data=payload, headers=headers)

    return response.text

if __name__ == "__main__":
    client = MongoClient('localhost', 27017)
    db = client.taller04

    url = 'http://api.meaningcloud.com/topics-2.0'
    licence_key = os.environ['MEANING_CLOUD_KEY']

    data = db.musicfans_topics.find({})
    for topic in data:        
        rs = extract_entities(licence_key, str(topic['summary'].encode('utf-8')))
        json_rs = json.loads(rs.encode('utf-8'))
        try:
            entities = json_rs['entity_list']
        except:
            entities = []
        db.musicfans_topics.update({"_id" : ObjectId(topic['_id'])}, {"$set" : {"entities" : entities}})
