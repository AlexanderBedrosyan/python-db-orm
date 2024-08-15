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


def get_houses(search_string=None):
    if search_string is None or search_string.strip() == '':
        return "No houses match your search."

    query = Q(motto__istartswith=search_string) | Q(name__istartswith=search_string)

    houses_needed = House.objects.filter(query)

    if not houses_needed:
        return "No houses match your search."

    information = []

    for house in houses_needed.order_by('-wins', 'name'):
        motto = 'N/A'

        if house.motto:
           motto = house.motto

        information.append(f'House: {house.name}, wins: {house.wins}, motto: {motto}')

    return '\n'.join(information)


def get_most_dangerous_house():
    if not House.objects.all() or not Dragon.objects.all():
        return 'No relevant data.'

    dangerous_house = House.objects.annotate(dragons_count=Count('dragon_houses')).order_by('-dragons_count', 'name').first()

    info = 'ruling' if dangerous_house.is_ruling else 'not ruling'

    return f"The most dangerous house is the House of {dangerous_house.name} with {dangerous_house.dragons_count} dragons. Currently {info} the kingdom."


def get_most_powerful_dragon():
    if not Dragon.objects.all():
        return "No relevant data."
    query = Q(is_healthy=True)

    dragon = Dragon.objects.annotate(num_quests=Count('quest_dragons')).filter(query).order_by('-power', 'name').first()

    if not dragon:
        return "No relevant data."


    return (f"The most powerful healthy dragon is {dragon.name} with a power level of {float(dragon.power):.1f}, breath type {dragon.breath}, "
            f"and {dragon.wins} wins, coming from the house of {dragon.house.name}. Currently participating in {dragon.num_quests} quests.")
