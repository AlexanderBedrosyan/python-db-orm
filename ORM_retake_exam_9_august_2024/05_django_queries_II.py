import os
from typing import List

import django
from datetime import date, datetime, timedelta

from django.db.models import Case, When, F, Value, CharField, Avg, QuerySet, Count, Sum, Q, Max, Min

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import *

def update_dragons_data():
    healthy_query = Q(is_healthy=False) & Q(power__gt=1.0)

    if not Dragon.objects.all():
        return "No changes in dragons data."

    unhealthy_dragons = Dragon.objects.filter(healthy_query)

    if not unhealthy_dragons:
        return "No changes in dragons data."

    counter = 0

    for dragon in unhealthy_dragons:
        dragon.power -= Decimal(0.1)
        dragon.is_healthy = True
        counter += 1

        dragon.save()

    min_power = Dragon.objects.aggregate(min_power=Min('power'))['min_power']

    return f"The data for {counter} dragon/s has been changed. The minimum power level among all dragons is {min_power:.1f}"


def get_earliest_quest():
    if not Quest.objects.all():
        return 'No relevant data.'

    earliest_quest = Quest.objects.order_by('start_time').first()
    day = earliest_quest.start_time.day
    month = earliest_quest.start_time.month
    year = earliest_quest.start_time.year
    all_dragons = [dragon.name for dragon in earliest_quest.dragons.all().order_by('-power', 'name')]
    avg_power = earliest_quest.dragons.aggregate(avg_power=Avg('power'))['avg_power'] if all_dragons else ''
    host_name = earliest_quest.host.name if earliest_quest.host else ''

    return f"The earliest quest is: {earliest_quest.name}, code: {earliest_quest.code}, start date: {day}.{month}.{year}, host: {host_name}. Dragons: {'*'.join(all_dragons)}. Average dragons power level: {avg_power:.2f}"


def announce_quest_winner(quest_code):
    if not Quest.objects.all():
        return 'No such quest.'

    query = Q(code=quest_code)

    winner = Quest.objects.filter(query).first()

    if not winner:
        return 'No such quest.'

    the_most_powerful_dragon = winner.dragons.order_by('-power', 'name').first()
    the_most_powerful_dragon.house.wins += 1
    the_most_powerful_dragon.house.save()

    the_most_powerful_dragon.wins += 1
    the_most_powerful_dragon.save()

    house_wins = the_most_powerful_dragon.house.wins
    dragon_wins = the_most_powerful_dragon.wins

    winner.delete()

    return f"The quest: {winner.name} has been won by dragon {the_most_powerful_dragon.name} from house {the_most_powerful_dragon.house.name}. The number of wins has been updated as follows: {dragon_wins} total wins for the dragon and {house_wins} total wins for the house. The house was awarded with {winner.reward:.2f} coins."
