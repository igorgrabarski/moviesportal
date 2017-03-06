import json
import urllib2


class Person:
    API_KEY = '1d6024f272ab343b950270c96503e08f'
    LANGUAGE = '&language=en-US'
    PERSON_PREFIX = 'https://api.themoviedb.org/3/person/'
    PERSON_MIDDLE = '?api_key='

    def __init__(self, _id):
        self.id = _id
        self.imdb_id = ''
        self.name = ''
        self.also_known_as = ''
        self.birthday = ''
        self.deathday = ''
        self.place_of_birth = ''
        self.popularity = ''
        self.profile_path = ''
        self.gender = ''
        self.adult = False
        self.homepage = ''
        self.biography = ''
        self.credit_cast_movies_id = []
        self.credit_crew_movies_id = []
        self.jobs = []
        self.person_images = []

    def get_person_by_id(self):

        self.parse_json(self.download_json(self.PERSON_PREFIX + str(self.id) +
                                           self.PERSON_MIDDLE + self.API_KEY + self.LANGUAGE))
        return self



    def search_people(self,query):
        pass

    def download_json(self, url):
        response = urllib2.urlopen(url)
        raw_input = response.read()

        response.close()

        return raw_input

    def parse_json(self, json_data):
        raw_json = json.loads(json_data)
        self.id = str(raw_json['id'])
        self.imdb_id = raw_json['imdb_id']
        self.name = raw_json['name']
        self.also_known_as = []

        for alias in raw_json['also_known_as']:
            self.also_known_as.append(alias)

        self.birthday = raw_json['birthday']
        self.deathday = raw_json['deathday']
        self.place_of_birth = raw_json['place_of_birth']
        self.popularity = raw_json['popularity']
        if not (raw_json['profile_path'] is None):
            self.profile_path = 'https://image.tmdb.org/t/p/w185' + raw_json['profile_path']

        if raw_json['gender'] == 1:
            self.gender = 'female'
        else:
            self.gender = 'male'

        self.adult = raw_json['adult']
        self.homepage = raw_json['homepage']
        self.biography = raw_json['biography']
        self.credit_cast_movies_id = []

        credit_data = self.download_json(self.PERSON_PREFIX + self.id + '/combined_credits?api_key=' +
                                         self.API_KEY + self.LANGUAGE)

        raw_credits = json.loads(credit_data)

        results = raw_credits['cast']

        for result in results:
            credit = result['id']
            self.credit_cast_movies_id.append(credit)

        self.credit_crew_movies_id = []
        self.jobs = []

        results = raw_credits['crew']

        for result in results:
            credit = result['id']
            job = result['job']
            self.credit_crew_movies_id.append(credit)
            self.jobs.append(job)

        self.person_images = []

        image_data = self.download_json(self.PERSON_PREFIX + self.id + '/images?api_key=' +
                                        self.API_KEY)

        raw_images = json.loads(image_data)

        results = raw_images['profiles']

        for result in results:
            image = 'https://image.tmdb.org/t/p/w185' + result['file_path']
            self.person_images.append(image)
