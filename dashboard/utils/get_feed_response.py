# coding: utf-8
import feedparser
from pymongo import MongoClient

if __name__ == "__main__":
    client = MongoClient('localhost', 27017)
    db = client.taller04

    # Accounts
    feeds = db.rss_musicfans.find({})
    topics = {}

    for feed in feeds:
        dto = db.musicfans_topics.find({'guid' : feed['article']['guid']})
        if dto.count() == 0:
            id = feed['article']['guid'].split('/')
            topic = {
                "id" : id[-1],
                "guid" : feed['article']['guid'],
                "title" : feed['article']['title'],
                "description" : feed['article']['description'],
                "summary" : feed['article']['summary'],
                "pubdate" : feed['article']['pubdate'],
                "link" : feed['article']['link'],
                "author" : feed['article']['author'],
                "author_link" : feed['article']['atom:author']['uri']['#'],
                "categories" : feed['article']['categories'],
            }

            # Obtener respuestas
            url = 'https://musicfans.stackexchange.com/feeds/question/' + id[-1]
            feed = feedparser.parse(url)
            responses = []
            for entry in feed.entries:
                if entry['title'].startswith('Answer'):
                    response = {
                        "title" : entry['title'],
                        "summary" : entry['summary'],
                        "pubdate" : entry['updated'],
                        "author" : entry['author_detail']['name'],
                        "author_link" : entry['author_detail']['href'],
                    }
                    responses.append(response)
            topic['responses'] = responses

            # print(topic)
            db.musicfans_topics.insert_one(topic)
