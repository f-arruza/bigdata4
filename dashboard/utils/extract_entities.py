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
        # title
        rs = extract_entities(licence_key, str(topic['title'].encode('utf-8')))
        json_rs = json.loads(rs.encode('utf-8'))
        try:
            entities = json_rs['entity_list']
        except:
            entities = []
        db.musicfans_topics.update({"_id" : ObjectId(topic['_id'])}, {"$set" : {"entities_title" : entities}})
        for dto in entities:
            db.entities.insert_one(dto)
        db.entities_total.insert_one(json_rs)

        # content - summary
        rs = extract_entities(licence_key, str(topic['summary'].encode('utf-8')))
        json_rs = json.loads(rs.encode('utf-8'))
        try:
            entities = json_rs['entity_list']
        except:
            entities = []
        db.musicfans_topics.update({"_id" : ObjectId(topic['_id'])}, {"$set" : {"entities" : entities}})
        for dto in entities:
            db.entities.insert_one(dto)
        db.entities_total.insert_one(json_rs)

        # responses
        index = 0
        for tp_response in topic['responses']:
            # title
            rs = extract_entities(licence_key, str(tp_response['title'].encode('utf-8')))
            json_rs = json.loads(rs.encode('utf-8'))
            try:
                entities = json_rs['entity_list']
            except:
                entities = []
            path = "responses." + str(index) + ".entities_title"
            db.musicfans_topics.update({"_id" : ObjectId(topic['_id'])}, {"$set" : {path : entities}})
            for dto in entities:
                db.entities.insert_one(dto)
            db.entities_total.insert_one(json_rs)

            # content - summary
            rs = extract_entities(licence_key, str(tp_response['summary'].encode('utf-8')))
            json_rs = json.loads(rs.encode('utf-8'))
            try:
                entities = json_rs['entity_list']
            except:
                entities = []
            path = "responses." + str(index) + ".entities"
            db.musicfans_topics.update({"_id" : ObjectId(topic['_id'])}, {"$set" : {path : entities}})
            for dto in entities:
                db.entities.insert_one(dto)
            db.entities_total.insert_one(json_rs)
            index = index + 1
