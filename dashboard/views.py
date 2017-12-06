# coding: utf-8
import json
import numpy
import requests
from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from bson.objectid import ObjectId
from pymongo import MongoClient

# Create your views here.
client = MongoClient('localhost', 27017)
db = client['taller04']

class IndexView(TemplateView):
    template_name = 'dashboard/index.html'

def summary(request):
    data = db['summary'].find_one({})
    data_musicfans = db['musicfans_topics'].aggregate([ { '$group': { '_id' : '$type', 'request_count' : { '$sum' : 1}, 'response_count' : { '$sum' : { "$size": "$responses" } } } } ])

    total_request_musicfans = 0
    total_response_musicfans = 0
    for dto in data_musicfans:
        total_request_musicfans = dto['request_count']
        total_response_musicfans = dto['response_count']

    perc_tweets_en = numpy.around((data['total_tweets_en'] / data['total_tweets']) * 100, 2)
    perc_tweets_es = numpy.around((data['total_tweets_es'] / data['total_tweets']) * 100, 2)
    json_data = {
        'total_tweets': data['total_tweets'],
        'total_rts': data['total_rts'],
        'perc_tweets_en' : perc_tweets_en,
        'perc_tweets_es' : perc_tweets_es,
        'total_accounts': data['total_accounts'],
        'total_hashtags': data['total_hashtags'],
        'total_quotes': data['total_quotes'],
        'total_request_musicfans' : total_request_musicfans,
        'total_response_musicfans' : total_response_musicfans,
    }
    return HttpResponse(json.dumps(json_data, ensure_ascii=False).encode('utf-8'),
                        content_type="application/json; charset=utf-8")

def accounts(request):
    limit = request.GET.get('limit')
    offset = request.GET.get('offset')

    if (limit is not None and offset is not None):
        data = db['accounts'].find({}).skip(int(offset)).limit(int(limit)).sort([('tweets_count', -1)])
        # print(data)
        result = []
        for dto in data:
            json_data = {
                'id': dto['id'],
                'name': dto['name'],
                'username': dto['username'],
                'location': dto['location'],
                'image': dto['image'],
                'description': dto['description'],
                'tweets_count': dto['tweets_count'],
                'rtweets_count': dto['rtweets_count'],
            }
            result.append(json_data)
    else:
        result = 'Limit and offset parameters not found.'
    return HttpResponse(json.dumps(result, ensure_ascii=False).encode('utf-8'),
                        content_type="application/json; charset=utf-8")

def hashtags(request):
    limit = request.GET.get('limit')
    offset = request.GET.get('offset')

    if (limit is not None and offset is not None):
        data = db['hashtags'].find({}).skip(int(offset)).limit(int(limit)).sort('count', -1)
        # print(data)
        result = []
        for dto in data:
            json_data = {
                'hashtag': dto['hashtag'],
                'count': dto['count'],
            }
            result.append(json_data)
    else:
        result = 'Limit and offset parameters not found.'
    return HttpResponse(json.dumps(result, ensure_ascii=False).encode('utf-8'),
                        content_type="application/json; charset=utf-8")

def locations(request):
    limit = request.GET.get('limit')
    offset = request.GET.get('offset')

    if (limit is not None and offset is not None):
        data = db['locations'].find({}).skip(int(offset)).limit(int(limit)).sort('count', -1)
        # print(data)
        result = []
        for dto in data:
            json_data = {
                'location': dto['location'],
                'count': dto['count'],
            }
            result.append(json_data)
    else:
        result = 'Limit and offset parameters not found.'
    return HttpResponse(json.dumps(result, ensure_ascii=False).encode('utf-8'),
                        content_type="application/json; charset=utf-8")

def quotes(request):
    limit = request.GET.get('limit')
    offset = request.GET.get('offset')

    if (limit is not None and offset is not None):
        data = db['quotes'].find({}).skip(int(offset)).limit(int(limit)).sort('count', -1)
        # print(data)
        result = []
        for dto in data:
            json_data = {
                'quote': dto['quote'],
                'count': dto['count'],
            }
            result.append(json_data)
    else:
        result = 'Limit and offset parameters not found.'
    return HttpResponse(json.dumps(result, ensure_ascii=False).encode('utf-8'),
                        content_type="application/json; charset=utf-8")

def polarities(request):
    data = db['polarities'].find({}).sort('polarity_id', 1)
    # print(data)
    result = []
    for dto in data:
        json_data = {
            'polarity_id': dto['polarity_id'],
            'polarity': dto['polarity'],
            'count': dto['count'],
        }
        result.append(json_data)
    return HttpResponse(json.dumps(result, ensure_ascii=False).encode('utf-8'),
                        content_type="application/json; charset=utf-8")

def tweets(request):
    limit = request.GET.get('limit')
    offset = request.GET.get('offset')
    query = request.GET.get('query')

    if (limit is not None and offset is not None):
        if query is not None:
            data = db['tweets'].find({'tweet.text':{'$regex':str(query)}}).skip(int(offset)).limit(int(limit))
        else:
            data = db['tweets'].find({}).skip(int(offset)).limit(int(limit))
        result = []
        for dto in data:
            try:
                location = dto['location']['place']
            except:
                location = "Sin información"

            json_data = {
                'time': dto['tweet']['created_at'],
                'text': dto['tweet']['text'],
                'account': dto['tweet']['user']['screen_name'],
                'location': location,
                'polarity_id': dto['polarity_id'],
                'polarity': dto['polarity'],
            }
            result.append(json_data)
    else:
        result = 'Limit and offset parameters not found.'
    return HttpResponse(json.dumps(result, ensure_ascii=False).encode('utf-8'),
                        content_type="application/json; charset=utf-8")

def musicfans(request):
    limit = request.GET.get('limit')
    offset = request.GET.get('offset')
    query = request.GET.get('query')

    if (limit is not None and offset is not None):
        if query is not None:
            data = db['musicfans_topics'].find({'summary':{'$regex':str(query)}}).skip(int(offset)).limit(int(limit))
        else:
            data = db['musicfans_topics'].find({}).skip(int(offset)).limit(int(limit))
        result = []
        for dto in data:
            json_data = {
                'id': dto['id'],
                'guid': dto['guid'],
                'title': dto['title'],
                'description': dto['description'],
                'summary': dto['summary'],
                'pubdate': dto['pubdate'].strftime("%Y-%m-%d %H:%M:%S"),
                'link': dto['link'],
                'author' : dto['author'],
                'author_link': dto['author_link'],
                'categories': dto['categories'],
                'responses': dto['responses'],
                'entities': dto['entities'],
                'entities_title': dto['entities_title'],
            }
            result.append(json_data)
    else:
        result = 'Limit and offset parameters not found.'
    return HttpResponse(json.dumps(result, ensure_ascii=False).encode('utf-8'),
                        content_type="application/json; charset=utf-8")

def musicfans_by_id(request, topic_id):
    data = db['musicfans_topics'].find({ '_id' : ObjectId(topic_id) })

    result = []
    for dto in data:
        json_data = {
            'id': dto['id'],
            'guid': dto['guid'],
            'title': dto['title'],
            'description': dto['description'],
            'summary': dto['summary'],
            'pubdate': dto['pubdate'].strftime("%Y-%m-%d %H:%M:%S"),
            'link': dto['link'],
            'author' : dto['author'],
            'author_link': dto['author_link'],
            'categories': dto['categories'],
            'responses': dto['responses'],
            'entities': dto['entities'],
            'entities_title': dto['entities_title'],
        }
        result.append(json_data)
    return HttpResponse(json.dumps(result, ensure_ascii=False).encode('utf-8'),
                        content_type="application/json; charset=utf-8")

def persons(request):
    topic_id = request.GET.get('topic_id')
    if (topic_id is not None):
        try:
            data = db['persons'].find({ 'topic_id' : ObjectId(topic_id) })
            result = []
            for dt in data:
                result.append({
                    'source' : dt['source'],
                    'data' : dt['data'],
                })
        except:
            result = 'topic_id incorrect.'
    else:
        result = 'topic_id parameter not found.'
    return HttpResponse(json.dumps(result, ensure_ascii=False).encode('utf-8'),
                        content_type="application/json; charset=utf-8")

def persons_spotify(request):
    topic_id = request.GET.get('topic_id')
    if (topic_id is not None):
        try:
            data = db['persons_spotify'].find({ 'topic_id' : ObjectId(topic_id) })
            result = []
            for dt in data:
                result.append({
                    'artist_id' : dt['artist_id'],
                    'name' : dt['name'],
                    'popularity' : dt['popularity'],
                    'type' : dt['type'],
                    'url' : dt['url'],
                    'followers' : dt['followers'],
                    'genres' : dt['genres'],
                    'images' : dt['images'],
                    'albums' : dt['albums'],
                })
        except:
            result = 'topic_id incorrect.'
    else:
        result = 'topic_id parameter not found.'
    return HttpResponse(json.dumps(result, ensure_ascii=False).encode('utf-8'),
                        content_type="application/json; charset=utf-8")

def organizations(request):
    topic_id = request.GET.get('topic_id')
    if (topic_id is not None):
        try:
            data = db['organizations'].find({ 'topic_id' : ObjectId(topic_id) })
            result = []
            for dt in data:
                result.append({
                    'source' : dt['source'],
                    'data' : dt['data'],
                })
        except:
            result = 'topic_id incorrect.'
    else:
        result = 'topic_id parameter not found.'
    return HttpResponse(json.dumps(result, ensure_ascii=False).encode('utf-8'),
                        content_type="application/json; charset=utf-8")

def locations_ent(request):
    topic_id = request.GET.get('topic_id')
    if (topic_id is not None):
        try:
            data = db['locations_ent'].find({ 'topic_id' : ObjectId(topic_id) })
            result = []
            for dt in data:
                result.append({
                    'source' : dt['source'],
                    'data' : dt['data'],
                })
        except:
            result = 'topic_id incorrect.'
    else:
        result = 'topic_id parameter not found.'
    return HttpResponse(json.dumps(result, ensure_ascii=False).encode('utf-8'),
                        content_type="application/json; charset=utf-8")

class TweetsView(TemplateView):
    template_name = 'dashboard/tweets.html'

    def get_context_data(self, **kwargs):
        context = super(TweetsView, self).get_context_data(**kwargs)
        context['tweets'] = db['tweets'].find({}).limit(5000)
        return context

class PolaritiesView(TemplateView):
    template_name = 'dashboard/polaridades.html'


class AccountsView(TemplateView):
    template_name = 'dashboard/cuentas.html'


class HastagsView(TemplateView):
    template_name = 'dashboard/hastags.html'

    def get_context_data(self, **kwargs):
        context = super(HastagsView, self).get_context_data(**kwargs)
        context['hashtags'] = db['hashtags'].find({}).limit(1000).sort('count', -1)
        return context


class LocationsView(TemplateView):
    template_name = 'dashboard/locations.html'

    def get_context_data(self, **kwargs):
        context = super(LocationsView, self).get_context_data(**kwargs)
        context['locations'] = db['locations'].find({}).limit(1000).sort('count', -1)
        return context


class QuotesView(TemplateView):
    template_name = 'dashboard/quotes.html'

    def get_context_data(self, **kwargs):
        context = super(QuotesView, self).get_context_data(**kwargs)
        context['quotes'] = db['quotes'].find({}).limit(1000).sort('count', -1)
        return context

def search_tweets(request):
    query = request.GET.get('query')
    start = request.GET.get('start')
    limit = request.GET.get('limit')

    if (start is None):
        start = 0
    if (limit is None):
        limit = 10
    if (query is None):
        q = '*:*'
    else:
        q = ''
        qparams = query.split(' ')
        print(qparams)
        for param in qparams:
            condition = 'payload:*' + param + '*'
            if q == '':
                q = condition
            else:
                q = q + ' or ' + condition
        if q != '':
            q = '(' + q + ')'

    url = 'http://172.24.100.95:8084/solr/tweets/select?q={}&rows={}&start={}'
    url = url.format(q, limit, start)
    response = requests.get(url)
    return HttpResponse(json.dumps(response.json()['response']['docs'],
                                   ensure_ascii=False).encode('utf-8'),
                        content_type="application/json; charset=utf-8")
