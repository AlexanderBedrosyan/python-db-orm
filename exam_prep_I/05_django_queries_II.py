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


def get_actors_by_movies_count():
    actors = Actor.objects.annotate(total_movies=Count('movies')).order_by('-total_movies', 'full_name')[0:3]

    if not Movie.objects.all() or not actors:
        return ''

    information = []
    for actor in actors:
        information.append(f"{actor.full_name}, participated in {actor.total_movies} movies")

    return '\n'.join(information)


def get_top_rated_awarded_movie():
    best_movie = Movie.objects\
                  .filter(is_awarded=True)\
                  .order_by('-rating', 'title')\
                  .first()

    if not best_movie:
        return ''

    starring_actor = best_movie.starring_actor

    if not starring_actor:
        starring_actor = 'N/A'
    else:
        starring_actor = starring_actor.full_name

    cast_actors = ', '.join(a.full_name for a in best_movie.actors.all().order_by('full_name'))

    if not cast_actors:
        cast_actors = ''

    return (f"Top rated awarded movie: {best_movie.title}, rating: {best_movie.rating:.1f}. Starring actor: "
            f"{starring_actor}. Cast: {cast_actors}.")


def increase_rating():
    query = Q(is_classic=True) & Q(rating__lt=10.0)
    all_classic_movies = Movie.objects.filter(query)

    if not all_classic_movies:
        return "No ratings increased."

    movies_to_update = []

    for movie in all_classic_movies:
        new_rating = movie.rating + Decimal(0.1)

        if new_rating > 10.0:
            new_rating = 10.0

        movie.rating = new_rating
        movies_to_update.append(movie)

    Movie.objects.bulk_update(movies_to_update, ['rating'])

    return f"Rating increased for {len(movies_to_update)} movies."
