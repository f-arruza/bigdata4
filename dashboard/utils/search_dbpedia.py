# coding: utf-8
from SPARQLWrapper import JSON, SPARQLWrapper

def get_semantic_data(entity):
    query_prefix = " PREFIX dbres: <http://dbpedia.org/resource/> "
    query_describe = " DESCRIBE dbres:" + entity + " LIMIT 1000"
    query = query_prefix + query_describe

    query = '''
    PREFIX db: <http://dbpedia.org/resource/>
    SELECT ?p ?o
    WHERE { db:''' + entity + ' ?p ?o } LIMIT 1000'

    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setReturnFormat(JSON)
    sparql.setQuery(query)

    return sparql.query().convert()

rs = get_semantic_data('Polanski')
print(rs)
