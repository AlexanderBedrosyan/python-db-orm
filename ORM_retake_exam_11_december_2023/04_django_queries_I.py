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


def get_tennis_players(search_name=None, search_country=None):
    if search_name is None and search_country is None:
        return ""

    query = Q()
    if search_name is not None:
        query &= Q(full_name__icontains=search_name)
    if search_country is not None:
        query &= Q(country__icontains=search_country)

    players = TennisPlayer.objects.filter(query).order_by('ranking')

    if not players.exists():
        return ""

    result = []
    for player in players:
        result.append(f"Tennis Player: {player.full_name}, country: {player.country}, ranking: {player.ranking}")
    return "\n".join(result)


def get_top_tennis_player():
    if not TennisPlayer.objects.all():
        return ''

    top_tennis = TennisPlayer.objects \
        .annotate(num_wins=Count('won_matches')) \
        .order_by('-num_wins', 'full_name') \
        .first()

    if not top_tennis:
        return ''

    return f"Top Tennis Player: {top_tennis.full_name} with {top_tennis.num_wins} wins."


def get_tennis_player_by_matches_count():
    if not Match.objects.all():
        return ''

    player_matches = TennisPlayer.objects \
        .annotate(num_of_matches=Count('match_players')) \
        .order_by('-num_of_matches', 'ranking') \
        .first()

    if not player_matches or player_matches.num_of_matches <= 0:
        return ''

    return f"Tennis Player: {player_matches.full_name} with {player_matches.num_of_matches} matches played."


