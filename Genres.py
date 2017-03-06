import urllib2
import json


class Genres:
    file = open('API_KEY')
    API_KEY = file.read()
    file.close()
    LANGUAGE = 'en-US'
    GENRES_URL = 'https://api.themoviedb.org/3/genre/movie/list?api_key=' + \
                 API_KEY + '&language=' + LANGUAGE

    def __init__(self):
        self.genres = []
        self.id = ''
        self.name = ''

    def get_genres(self):
        return self.parse_json(self.download_json())

    def get_genre_by_id(self, id):
        genres = self.get_genres()

        for genre in genres:
            if genre.id == id:
                return genre.name

        return 'unknown'

    def download_json(self):
        response = urllib2.urlopen(self.GENRES_URL)

        raw_data = response.read()

        response.close()

        return raw_data

    def parse_json(self, json_data):
        raw_json = json.loads(json_data)
        results = raw_json['genres']

        genres = []
        for result in results:
            genre = Genres()
            genre.id = str(result['id'])
            genre.name = result['name']
            genres.append(genre)

        return genres
