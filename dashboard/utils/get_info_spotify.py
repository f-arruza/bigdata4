# coding: utf-8
import os
import spotipy
from pymongo import MongoClient

token = os.environ['SPOTIFY_TOKEN']
sp = spotipy.Spotify(auth=token)

def show_artist_albums(artist_id):
    albums = []
    results = sp.artist_albums(artist_id, album_type='album')

    for album in results['items']:
        data_json = {
            'album_id' : album['id'],
            'name' : album['name'],
            'url' : album['external_urls']['spotify'],
            'images' : album['images'],
        }
        albums.append(data_json)
    return albums

if __name__ == "__main__":
    client = MongoClient('localhost', 27017)
    db = client.taller04

    data = db.persons.find({})
    for person in data:
        name = person['data']['name']
        result = sp.search(q=name, type='artist')

        for artist in result['artists']['items']:
            data_json = {
                'topic_id' : person['topic_id'],
                'artist_id' : artist['id'],
                'name' : artist['name'],
                'popularity' : artist['popularity'],
                'type' : artist['type'],
                'url' : artist['external_urls']['spotify'],
                'followers' : artist['followers']['total'],
                'genres' : artist['genres'],
            }
            images = []
            for imag in artist['images']:
                images.append(imag['url'])
            data_json['images'] = images

            # Albums
            albums = show_artist_albums(artist['id'])
            data_json['albums'] = albums

            db.persons_spotify.insert_one(data_json)
