# coding: utf-8
import re
from bson.objectid import ObjectId
from pymongo import MongoClient
from SPARQLWrapper import JSON, SPARQLWrapper

def clear_text(text):
	clear = text.strip()
	clear = re.sub('[^a-zA-Z0-9 \n]', '', clear)
	return clear.replace(' ', '_')

def get_data_object(semantic_object):
    if semantic_object['type'] == 'uri':
        value = semantic_object['value']
        value = value.replace('http://dbpedia.org/resource/', '')
        return value.replace('_',' ')
    if 'literal' in semantic_object['type']:
        return str(semantic_object['value'])
    return ''

def query_sparkql(entity):
    query = ' PREFIX db: <http://dbpedia.org/resource/>'\
            ' SELECT ?p ?o'\
            ' WHERE { db:''' + entity + ' ?p ?o } LIMIT 1000'

    da = SPARQLWrapper('http://dbpedia.org/sparql')
    da.setReturnFormat(JSON)
    da.setQuery(query)
    return da.query().convert()

def search_person(person):
    semantic_data = query_sparkql(clear_text(person))

    person_data = {}
    occupations = []
    genres = []

    for relation in semantic_data['results']['bindings']:
        if relation['p']['value'] == 'http://dbpedia.org/ontology/birthPlace':
            person_data['birthplace'] = get_data_object(relation['o'])
        if relation['p']['value'] == 'http://dbpedia.org/ontology/birthDate':
            person_data['birthdate'] = get_data_object(relation['o'])
        if relation['p']['value'] == 'http://dbpedia.org/ontology/deathPlace':
            person_data['deathplace'] = get_data_object(relation['o'])
        if relation['p']['value'] == 'http://dbpedia.org/ontology/deathDate':
            person_data['deathdate'] = get_data_object(relation['o'])
        if relation['p']['value'] == 'http://xmlns.com/foaf/0.1/gender':
            person_data['gender'] = get_data_object(relation['o'])
        if relation['p']['value'] == 'http://xmlns.com/foaf/0.1/isPrimaryTopicOf':
            person_data['page'] = get_data_object(relation['o'])
        if relation['p']['value'] == 'http://dbpedia.org/property/occupation':
            occupations.append(get_data_object(relation['o']))
        if relation['p']['value'] == 'http://dbpedia.org/ontology/genre':
            genres.append(get_data_object(relation['o']))

    if len(semantic_data['results']['bindings']) > 0:
        person_data['name'] = person
        person_data['occupations'] = occupations
        person_data['genre'] = genres
        return person_data
    else:
        return None

def search_persons(topic_id, data):
    # title - entities
    for ent_title in data['entities_title']:
        type = ent_title['sementity']['type']

        # Person
        if type.startswith('Top>Person>'):
            dto = db.persons.find({'topic_id' : topic_id, 'data.name' : ent_title['form']})
            if dto.count() == 0:
                person_data = search_person(ent_title['form'])
                if person_data is not None:
                    db.persons.insert_one({
                        'topic_id' : topic_id,
                        'source' : 'dbpedia',
                        'data' : person_data
                    })

    # summary - entities
    for ent_title in data['entities']:
        type = ent_title['sementity']['type']

        # Person
        if type.startswith('Top>Person>'):
            dto = db.persons.find({'topic_id' : topic_id, 'data.name' : ent_title['form']})
            if dto.count() == 0:
                person_data = search_person(ent_title['form'])
                if person_data is not None:
                    db.persons.insert_one({
                        'topic_id' : topic_id,
                        'source' : 'dbpedia',
                        'data' : person_data
                    })


if __name__ == "__main__":
    client = MongoClient('localhost', 27017)
    db = client.taller04

    data = db.musicfans_topics.find({})
    for topic in data:
        # topic - request
        search_persons(ObjectId(topic['_id']), topic)
        # responses
        for resp in topic['responses']:
            search_persons(ObjectId(topic['_id']), resp)
