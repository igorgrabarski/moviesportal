import json
import urllib2
from types import NoneType

import Movie
from Service import Service


class Movies:
    # Please enter your API KEY below:
    API_KEY = '1d6024f272ab343b950270c96503e08f'
    LANGUAGE = 'en-US'
    INITIAL_PREFIX = 'https://api.themoviedb.org/3/'
    MOVIE_PREFIX = 'movie/'
    TV_PREFIX = 'tv/'

    is_tv_show = False
    total_results = 0
    total_pages = 0
    download_errors = 0
    parsing_errors = 0

    POPULAR_MOVIE_URL = INITIAL_PREFIX + MOVIE_PREFIX + 'popular?api_key=' + \
                        API_KEY + '&language=' + LANGUAGE + \
                        '&page='
    NOW_PLAYING_MOVIE_URL = INITIAL_PREFIX + MOVIE_PREFIX + 'now_playing?api_key=' + \
                            API_KEY + '&language=' + LANGUAGE + \
                            '&page='

    TOP_RATED_MOVIE_URL = INITIAL_PREFIX + MOVIE_PREFIX + 'top_rated?api_key=' + \
                          API_KEY + '&language=' + LANGUAGE + \
                          '&page='

    UPCOMING_MOVIE_URL = INITIAL_PREFIX + MOVIE_PREFIX + 'upcoming?api_key=' + \
                         API_KEY + '&language=' + LANGUAGE + \
                         '&page='

    POPULAR_TV_URL = INITIAL_PREFIX + TV_PREFIX + 'popular?api_key=' + \
                     API_KEY + '&language=' + LANGUAGE + \
                     '&page='

    TOP_RATED_TV_URL = INITIAL_PREFIX + TV_PREFIX + 'top_rated?api_key=' + \
                       API_KEY + '&language=' + LANGUAGE + \
                       '&page='

    ON_THE_AIR_TV_URL = INITIAL_PREFIX + TV_PREFIX + 'on_the_air?api_key=' + \
                        API_KEY + '&language=' + LANGUAGE + \
                        '&page='

    AIRING_TODAY_TV_URL = INITIAL_PREFIX + TV_PREFIX + 'airing_today?api_key=' + \
                          API_KEY + '&language=' + LANGUAGE + \
                          '&page='

    SMALL_IMAGE_URL_PREFIX = 'https://image.tmdb.org/t/p/w185'
    LARGE_IMAGE_URL_PREFIX = 'https://image.tmdb.org/t/p/w500'



# =============================================== CONSTRUCTOR ==================================================================


    def __init__(self, movie_type):

        if movie_type == 'popular_movies':
            self.movie_url = self.POPULAR_MOVIE_URL
        elif movie_type == 'now_playing_movies':
            self.movie_url = self.NOW_PLAYING_MOVIE_URL
        elif movie_type == 'top_rated_movies':
            self.movie_url = self.TOP_RATED_MOVIE_URL
        elif movie_type == 'upcoming_movies':
            self.movie_url = self.UPCOMING_MOVIE_URL
        elif movie_type == 'popular_tv':
            self.movie_url = self.POPULAR_TV_URL
        elif movie_type == 'top_rated_tv':
            self.movie_url = self.TOP_RATED_TV_URL
        elif movie_type == 'on_the_air_tv':
            self.movie_url = self.ON_THE_AIR_TV_URL
        else:
            self.movie_url = self.TOP_RATED_MOVIE_URL


# =============================================== GRTMOVIES ==================================================================


    def get_movies(self, pages):

        movies = []

        for cycle in range(0, len(pages)):
            try:
                movies.extend(self.parse_json(self.download_json(self.movie_url +
                                                                 '&page=' + str(pages[cycle]))))
            except Exception as exc:
                self.download_errors += 1
                Service.write_to_log('\nWrong page number' + format(exc.message))

        self.download_errors = 0
        return movies

# =============================================== GET MOVIES BY KEYWORDS==================================================================



    def get_movies_by_keywords(self, keywords):
        pass

# =============================================== GET SIMILAR MOVIES ==================================================================


    # Resource types are movie or tv
    def get_similar_movies(self, movie_id, resource_type, pages=1):

        if resource_type == 'movie':
            url = self.INITIAL_PREFIX + 'movie/' + str(movie_id) + '/similar?api_key=' \
                  + self.API_KEY + '&language=' + self.LANGUAGE + '&page=' + str(pages)

        elif resource_type == 'tv':
            url = self.INITIAL_PREFIX + 'tv/' + str(movie_id) + '/similar?api_key=' \
                  + self.API_KEY + '&language=' + self.LANGUAGE + '&page=' + str(pages)
        else:
            return None

        return self.parse_json(self.download_json(url))


#=============================================== SEARCH ==================================================================

    # Resource types are movie or tv
    def search_movies(self,resource_type,query,page=1):

        query=query.replace(' ', '%20')


        url=self.INITIAL_PREFIX+'search/'+resource_type+'?api_key='+self.API_KEY+'&language='+self.LANGUAGE+'&query='+\
            query+'&page='+str(page)

        return self.parse_json(self.download_json(url))

# =============================================== DOWNLOAD ==================================================================


    def download_json(self, url):
        raw_data = None
        try:
            response = urllib2.urlopen(url)

            raw_data = response.read()

            response.close()
        except Exception as exc:
            self.download_errors += 1
            Service.write_to_log('\nFailed to download JSON file.\n' + format(exc.message))

        return raw_data

    # =============================================== PARSE ==================================================================


    def parse_json(self, json_data):

        results = None
        try:
            raw_json = json.loads(json_data)
            if 'results' in raw_json:
                results = raw_json['results']
            elif len(raw_json) > 1:
                results = raw_json
            else:
                return None



        except Exception as exc:
            self.parsing_errors += 1
            Service.write_to_log('\nFailed to parse results\n' + format(exc.message))

        movies = []

        for result in results:

            movie = Movie.Movie()
            try:

                movie.total_results = raw_json['total_results']
                movie.total_pages = raw_json['total_pages']

                movie.id = str(result['id'])

                if result['poster_path'] is None:
                    movie.poster_path = ''
                else:
                    movie.poster_path = result['poster_path']

                if result['backdrop_path'] is None:
                    movie.backdrop_path = ''

                else:
                    movie.backdrop_path = result['backdrop_path']

                movie.popularity = result['popularity']
                movie.vote_count = result['vote_count']
                movie.vote_average = result['vote_average']

                if movie.vote_average is not None:
                    movie.full_star = int(movie.vote_average / 2)
                    if (movie.vote_average - (int(movie.vote_average))) >= 0.5:
                        movie.full_star += 1

                else:
                    movie.full_star = 0

                if 'name' in result:
                    movie.title = result['name']
                    movie.movie_type='tv'

                if 'title' in result:
                    movie.title = result['title']
                    movie.movie_type='movie'

                if 'media_type' in result:
                    movie.media_type = result['media_type']

                movies.append(movie)

            except Exception as exc:
                self.parsing_errors += 1
                Service.write_to_log('\nFailed to parse movie\n' + format(exc.message))
                continue

            Service.write_to_log('\nDownload errors : ' + str(self.download_errors) +
                                 '\nParsing errors : ' + str(self.parsing_errors) + '\n')
            self.download_errors = 0;
            self.parsing_errors = 0

        return movies


