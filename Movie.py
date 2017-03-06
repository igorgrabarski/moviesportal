import urllib2
import json
import Review
import Trailer
import Person
from Service import Service


class Movie:
    API_KEY = '1d6024f272ab343b950270c96503e08f'
    LANGUAGE = 'en-US'
    INITIAL_PREFIX = 'https://api.themoviedb.org/3/'

    YOU_TUBE_PREFIX = 'https://www.youtube.com/embed/'
    IMDB_PREFIX = 'http://www.imdb.com/title/'

    SEARCH_PREFIX = 'search/multi?api_key='
    SEARCH_REQUEST_URL = INITIAL_PREFIX + SEARCH_PREFIX + API_KEY + '&language=' + LANGUAGE + '&query='

    def __init__(self):
        self.id = ''
        self.imdb_id = ''
        self.title = ''
        self.original_title = ''
        self.poster_path = ''
        self.backdrop_path = ''
        self.overview = ''
        self.tagline = ''
        self.release_date = ''
        self.original_language = ''
        self.popularity = 0.00
        self.vote_count = 0
        self.vote_average = 0.00
        self.full_star=0
        self.video = False
        self.adult = False
        self.genre_ids = []
        self.first_air_date = ''
        self.last_air_date = ''
        self.budget = 0
        self.revenue = 0
        self.homepage = ''
        self.production_companies = []
        self.production_countries = []
        self.runtime = 0
        self.spoken_languages = []
        self.status = ''
        self.type = ''
        self.seasons = []
        self.number_of_seasons = 0
        self.number_of_episodes = 0
        self.networks = []
        self.in_production = False
        self.created_by = []
        self.movie_type = 'movie'
        total_results = 0
        total_pages = 0

        # Three media types are supported:
        # movie
        # tv
        # person


        self.origin_country = ''
        self.person = Person.Person('')

    def get_movie_by_id(self, resource_type, movie_id):

        resource_url = self.INITIAL_PREFIX + resource_type + '/' \
                       + str(movie_id) + '?api_key=' + self.API_KEY + '&language=' + self.LANGUAGE

        return self.parse_json(self.download_json(resource_url), resource_type)

    def get_alternative_titles(self):
        pass

    def get_credits(self, resource_type, movie_id):
        resource_url = self.INITIAL_PREFIX + resource_type + '/' + str(
            movie_id) + '/credits?api_key=' + self.API_KEY + '&language=' + self.LANGUAGE

        return self.parse_json(self.download_json(resource_url), 'credits')

    def get_keywords(self):
        pass

    def get_recommendations(self):
        pass

    def get_lists(self):
        pass

    def rate_movie(self):
        pass

    # 'movie' resource type available only
    def get_reviews(self, resource_type, id):
        resource_url = self.INITIAL_PREFIX + resource_type + '/' \
                       + str(id) + '/reviews?api_key=' + self.API_KEY + '&language=' + self.LANGUAGE

        return self.parse_json(self.download_json(resource_url), 'review')

    # Both 'movie' and 'tv' resource types available
    def get_trailers(self, resource_type, id):
        resource_url = self.INITIAL_PREFIX + resource_type + '/' \
                       + str(id) + '/videos?api_key=' + self.API_KEY + '&language=' + self.LANGUAGE

        return self.parse_json(self.download_json(resource_url), 'trailer')

    def download_json(self, resource_url):

        try:
            response = urllib2.urlopen(resource_url)
            raw_data = response.read()
            response.close()

        except urllib2.URLError as err:
            raise IOError('Movie not found. Wrong id number.')
        return raw_data

    def parse_json(self, json_data, resource_type):

        raw_json = json.loads(json_data)




        if resource_type == 'review':
            reviews = []

            results = raw_json['results']

            for result in results:

                if 'id' in result:
                    review = Review.Review()
                    review.movie_id = raw_json['id']
                    review.review_id = result['id']
                    review.author = result['author']
                    review.content = result['content']
                    review.url = result['url']
                    reviews.append(review)

                else:
                    continue

            return reviews

        elif resource_type == 'trailer':
            trailers = []
            results = raw_json['results']
            for result in results:

                if 'id' in result:
                    trailer = Trailer.Trailer()
                    trailer.movie_id = raw_json['id']
                    trailer.trailer_id = result['id']
                    trailer.url = self.YOU_TUBE_PREFIX + result['key']
                    trailer.name = result['name']
                    trailer.site = result['site']
                    trailer.size = result['size']
                    trailer.type = result['type']
                    trailers.append(trailer)

                else:
                    continue

            return trailers

        elif resource_type == 'movie':
            try:

                movie = Movie()
                movie.movie_type = 'movie'
                movie.id = str(raw_json['id'])
                movie.title = raw_json['title']
                movie.imdb_id = self.IMDB_PREFIX+raw_json['imdb_id']+'/'
                movie.original_title = raw_json['original_title']
                movie.poster_path = raw_json['poster_path']
                movie.backdrop_path = raw_json['backdrop_path']
                movie.overview = raw_json['overview']
                movie.tagline = raw_json['tagline']
                movie.release_date = raw_json['release_date']
                movie.original_language = raw_json['original_language']
                movie.popularity = raw_json['popularity']
                movie.vote_count = raw_json['vote_count']
                movie.vote_average = raw_json['vote_average']

                if movie.vote_average is not None:
                    movie.full_star = int(movie.vote_average / 2)
                    if (movie.vote_average - (int(movie.vote_average))) >= 0.5:
                        movie.full_star += 1

                else:
                    movie.full_star = 0


                movie.video = raw_json['video']
                movie.adult = raw_json['adult']
                movie.genre_ids = raw_json['genres']
                movie.budget = raw_json['budget']
                movie.revenue = raw_json['revenue']
                movie.homepage = raw_json['homepage']
                movie.production_companies = raw_json['production_companies']
                movie.production_countries = raw_json['production_countries']
                movie.runtime = raw_json['runtime']
                movie.spoken_languages = raw_json['spoken_languages']
                movie.status = raw_json['status']

            except Exception as exc:
                print(str(exc))
                pass

            return movie


        elif resource_type == 'tv':

            try:

                tv_show = Movie()
                tv_show.movie_type = 'tv'
                tv_show.id = str(raw_json['id'])
                tv_show.title = raw_json['name']
                tv_show.original_title = raw_json['original_name']
                tv_show.poster_path = raw_json['poster_path']
                tv_show.backdrop_path = raw_json['backdrop_path']
                tv_show.overview = raw_json['overview']
                tv_show.first_air_date = raw_json['first_air_date']
                tv_show.original_language = raw_json['original_language']
                tv_show.popularity = raw_json['popularity']
                tv_show.vote_count = raw_json['vote_count']
                tv_show.vote_average = raw_json['vote_average']

                if tv_show.vote_average is not None:
                    tv_show.full_star = int(tv_show.vote_average / 2)
                    if (tv_show.vote_average - (int(tv_show.vote_average))) >= 0.5:
                        tv_show.full_star += 1

                else:
                    tv_show.full_star = 0

                tv_show.genre_ids = raw_json['genres']
                tv_show.homepage = raw_json['homepage']
                tv_show.production_companies = raw_json['production_companies']
                tv_show.production_countries = raw_json['origin_country']
                tv_show.runtime = raw_json['episode_run_time']
                tv_show.original_language = raw_json['original_language']
                tv_show.created_by = raw_json['created_by']
                tv_show.in_production = raw_json['in_production']
                tv_show.last_air_date = raw_json['last_air_date']
                tv_show.networks = raw_json['networks']
                tv_show.number_of_episodes = raw_json['number_of_episodes']
                tv_show.number_of_seasons = raw_json['number_of_seasons']
                tv_show.seasons = raw_json['seasons']
                tv_show.status = raw_json['status']
                tv_show.type = raw_json['type']
                tv_show.origin_country = raw_json['origin_country']


            except Exception as exc:
                print(str(exc))
                pass

            return tv_show


        elif resource_type == 'credits':
            pass


        else:
            return None
