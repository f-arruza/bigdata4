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

def get_data_point(point):
	point = point.replace('POINT(','')
	point = point.replace(')','')
	point = point.replace(')','')
	coordinates = point.split()
	return coordinates[0],coordinates[1]

def query_sparkql(entity):
    query = ' PREFIX db: <http://dbpedia.org/resource/>'\
            ' SELECT ?p ?o'\
            ' WHERE { db:''' + entity + ' ?p ?o } LIMIT 10000'

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

def search_organization(organization):
    semantic_data = query_sparkql(clear_text(organization))

    org_data = {}
    services = []
    products = []
    places = []
    persons = []
    abstract = None

    for relation in semantic_data['results']['bindings']:
        if relation['p']['value'] == 'http://dbpedia.org/property/locationCity':
            org_data['city'] = get_data_object(relation['o'])
        if relation['p']['value'] == 'http://dbpedia.org/property/locationCountry':
            org_data['country'] = get_data_object(relation['o'])
        if relation['p']['value'] == 'http://dbpedia.org/ontology/type':
            org_data['type'] = get_data_object(relation['o'])
        if relation['p']['value'] == 'http://dbpedia.org/ontology/service':
            services.append(get_data_object(relation['o']))
        if relation['p']['value'] == 'http://dbpedia.org/ontology/product':
            products.append(get_data_object(relation['o']))
        if relation['p']['value'] == 'http://dbpedia.org/ontology/foundationPlace':
            places.append(get_data_object(relation['o']))
        if relation['p']['value'] == 'http://dbpedia.org/ontology/wikiPageExternalLink':
            org_data['page'] = get_data_object(relation['o'])
        if relation['p']['value'] == 'http://xmlns.com/foaf/0.1/name':
            org_data['fullname'] = get_data_object(relation['o'])
        if relation['p']['value'] == 'http://dbpedia.org/ontology/abstract' and abstract is None:
            abstract = get_data_object(relation['o'])
        if relation['p']['value'] == 'http://dbpedia.org/ontology/keyPerson':
            persons.append(get_data_object(relation['o']))

    if len(semantic_data['results']['bindings']) > 0:
        org_data['name'] = organization
        org_data['abstract'] = abstract
        org_data['services'] = services
        org_data['products'] = products
        org_data['places'] = places
        org_data['persons'] = persons
        return org_data
    else:
        return None

def search_location(location):
    semantic_data = query_sparkql(clear_text(location))

    location_data = {}
    coordinates = []

    for relation in semantic_data['results']['bindings']:
        if relation['p']['value'] == 'http://dbpedia.org/ontology/country':
            location_data['country'] = get_data_object(relation['o'])
        if relation['p']['value'] == 'http://xmlns.com/foaf/0.1/name':
            location_data['fullname'] = get_data_object(relation['o'])
        if relation['p']['value'] == 'http://xmlns.com/foaf/0.1/homepage':
            location_data['page'] = get_data_object(relation['o'])
        if relation['p']['value'] == 'http://www.w3.org/2003/01/geo/wgs84_pos#geometry':
            point = get_data_point(relation['o']['value'])
            coordinates.append( { 'lat' : point[0], 'lon' : point[1] })
        if relation['p']['value'] == 'http://dbpedia.org/ontology/PopulatedPlace/areaTotal':
            location_data['area'] = get_data_object(relation['o'])
        if relation['p']['value'] == 'http://dbpedia.org/ontology/capital':
            location_data['capital'] = get_data_object(relation['o'])
        if relation['p']['value'] == 'http://dbpedia.org/ontology/populationTotal':
            location_data['population'] = get_data_object(relation['o'])
        if relation['p']['value'] == 'http://dbpedia.org/property/countryCode':
            location_data['code'] = get_data_object(relation['o'])
        if relation['p']['value'] == 'http://dbpedia.org/property/currencyCode':
            location_data['currency'] = get_data_object(relation['o'])

    if len(semantic_data['results']['bindings']) > 0:
        location_data['name'] = location
        location_data['coordinates'] = coordinates
        return location_data
    else:
        return None

def enrich_data(topic_id, data):
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
        # Organization
        if type.startswith('Top>Organization>'):
            dto = db.organizations.find({'topic_id' : topic_id, 'data.name' : ent_title['form']})
            if dto.count() == 0:
                org_data = search_organization(ent_title['form'])
                if org_data is not None:
                    db.organizations.insert_one({
                        'topic_id' : topic_id,
                        'source' : 'dbpedia',
                        'data' : org_data
                    })
        # Location
        if type.startswith('Top>Location>'):
            dto = db.locations_ent.find({'topic_id' : topic_id, 'data.name' : ent_title['form']})
            if dto.count() == 0:
                location_data = search_location(ent_title['form'])
                if location_data is not None:
                    db.locations_ent.insert_one({
                        'topic_id' : topic_id,
                        'source' : 'dbpedia',
                        'data' : location_data
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
        # Organization
        if type.startswith('Top>Organization>'):
            dto = db.organizations.find({'topic_id' : topic_id, 'data.name' : ent_title['form']})
            if dto.count() == 0:
                org_data = search_organization(ent_title['form'])
                if org_data is not None:
                    db.organizations.insert_one({
                        'topic_id' : topic_id,
                        'source' : 'dbpedia',
                        'data' : org_data
                    })
        # Location
        if type.startswith('Top>Location>'):
            dto = db.locations_ent.find({'topic_id' : topic_id, 'data.name' : ent_title['form']})
            if dto.count() == 0:
                location_data = search_location(ent_title['form'])
                if location_data is not None:
                    db.locations_ent.insert_one({
                        'topic_id' : topic_id,
                        'source' : 'dbpedia',
                        'data' : location_data
                    })


if __name__ == "__main__":
    client = MongoClient('localhost', 27017)
    db = client.taller04

    data = db.musicfans_topics.find({})
    for topic in data:
        # topic - request
        enrich_data(ObjectId(topic['_id']), topic)
        # responses
        for resp in topic['responses']:
            enrich_data(ObjectId(topic['_id']), resp)
