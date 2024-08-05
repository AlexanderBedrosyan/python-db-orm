import os

import django
from django.db.models import Q, Count

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import TennisPlayer, Tournament, Match


# Create queries within functions
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


# Test get_tennis_player
def get_top_tennis_player():
    player = TennisPlayer.objects.annotate(
        num_of_wins=Count('matches_won')
    ).order_by('-num_of_wins', 'full_name').first()

    if not player:
        return ""

    return f"Top Tennis Player: {player.full_name} with {player.num_of_wins} wins."


def get_tennis_player_by_matches_count():
    player = TennisPlayer.objects.annotate(
        count_matches=Count('match')
    ).order_by('-count_matches', 'ranking').first()

    if player and player.count_matches > 0:
        return f"Tennis Player: {player.full_name} with {player.count_matches} matches played."
    return ""


# Django queries II
def get_tournaments_by_surface_type(surface=None):
    if surface is None:
        return ""

    tournaments = Tournament.objects.filter(
        surface_type__icontains=surface
    ).order_by(
        '-start_date'
    )

    if not tournaments:
        return ""

    result = []
    for tournament in tournaments:
        num_matches = tournament.match_set.count()
        result.append(f"Tournament: {tournament.name}, "
                      f"start date: {tournament.start_date}, "
                      f"matches: {num_matches}")

    return "\n".join(result)


def get_latest_match_info():
    match = Match.objects.order_by('-date_played', '-id').first()

    if not match:
        return ""

    return (f'Latest match played on: {match.date_played}, '
            f'tournament: {match.tournament.name}, '
            f'score: {match.score}, '
            f'players: {" vs ".join([player.full_name for player in match.players.all()])}, '
            f'winner: {"TBA" if not match.winner else match.winner.full_name}, '
            f'summary: {match.summary}')


def get_matches_by_tournament(tournament_name=None):
    if tournament_name is None:
        return "No matches found."

    try:
        tournament = Tournament.objects.get(name=tournament_name)
    except Tournament.DoesNotExist:
        return "No matches found."

    matches = tournament.match_set.order_by('-date_played')

    if not matches:
        return "No matches found."

    result = []

    for match in matches:
        result.append(f'Match played on: {match.date_played}, '
                      f'score: {match.score}, '
                      f'winner: {"TBA" if not match.winner else match.winner.full_name}')

    return "\n".join(result)