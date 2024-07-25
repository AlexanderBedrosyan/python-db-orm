import os
from typing import List

import django
from datetime import date, datetime, timedelta

from django.db.models import Case, When, F, Value, CharField, Avg, QuerySet, Count, Sum, Q, Max

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import *


def get_directors(search_name=None, search_nationality=None):
    query = None
    if search_name and search_nationality:
        query = Q(full_name__icontains=search_name) & Q(nationality__icontains=search_nationality)
    elif search_name and not search_nationality:
        query = Q(full_name__icontains=search_name)
    elif search_nationality and not search_name:
        query = Q(nationality__icontains=search_nationality)
    else:
        return ''

    directors = Director.objects.filter(query).order_by('full_name')

    if not directors:
        return ''

    information = []

    for d in directors:
        information.append(
            f'Director: {d.full_name}, nationality: {d.nationality}, experience: {d.years_of_experience}'
        )

    return '\n'.join(information)


def get_top_director():
    top_director = Director.objects.annotate(movies_number=Count('movie')).order_by('-movies_number', 'full_name').first()

    if not top_director:
        return ''

    movies = len(top_director.movie_set.all())

    return f"Top Director: {top_director.full_name}, movies: {movies}."


def get_top_actor():
    top_actor = Actor.objects.annotate(
        total_starring_movies=Count('starring_movies'),
        movies_avg_rating=Avg('starring_movies__rating')
    ) \
        .order_by('-total_starring_movies', 'full_name') \
        .first()

    if not Movie.objects.all() or not top_actor:
        return ""

    top_actor_movies = ', '.join([m.title for m in top_actor.starring_movies.all()])

    return f"Top Actor: {top_actor.full_name}, starring in movies: {top_actor_movies}, " \
           f"movies average rating: {top_actor.movies_avg_rating:.1f}"
