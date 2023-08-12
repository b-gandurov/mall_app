import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mall_app.settings')
import django

django.setup()
from mall_app.cinema.models import Movie

import datetime


def generate_movies():
    movie_data = [
        {'movie_name': 'Matrix 4', 'movie_type': 'Sci-Fi', 'duration': datetime.timedelta(minutes=150)},
        {'movie_name': 'John Wick 4', 'movie_type': 'Action', 'duration': datetime.timedelta(minutes=120)},
        {'movie_name': 'Dune', 'movie_type': 'Adventure', 'duration': datetime.timedelta(minutes=155)},
        {'movie_name': 'No Time To Die', 'movie_type': 'Action', 'duration': datetime.timedelta(minutes=163)},
        {'movie_name': 'Black Widow', 'movie_type': 'Action', 'duration': datetime.timedelta(minutes=134)},
        {'movie_name': 'A Quiet Place Part II', 'movie_type': 'Horror', 'duration': datetime.timedelta(minutes=97)},
        {'movie_name': 'Luca', 'movie_type': 'Animation', 'duration': datetime.timedelta(minutes=95)},
        {'movie_name': 'The Conjuring: The Devil Made Me Do It', 'movie_type': 'Horror',
         'duration': datetime.timedelta(minutes=112)},
        {'movie_name': 'Jungle Cruise', 'movie_type': 'Adventure', 'duration': datetime.timedelta(minutes=127)},
        {'movie_name': 'The French Dispatch', 'movie_type': 'Comedy', 'duration': datetime.timedelta(minutes=108)}
    ]

    for movie in movie_data:
        Movie.objects.create(**movie)


generate_movies()
