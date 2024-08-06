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


def get_astronauts(search_string=None):
    if search_string is None:
        return ''

    query = Q(name__icontains=search_string) | Q(phone_number__icontains=search_string)

    astronauts = Astronaut.objects.filter(query).order_by('name')

    if not astronauts:
        return ''

    information = []

    for a in astronauts:
        status = 'Active' if a.is_active else 'Inactive'
        information.append(f"Astronaut: {a.name}, phone number: {a.phone_number}, status: {status}")

    return '\n'.join(information)


def get_top_astronaut():
    if not Astronaut.objects.all() or not Mission.objects.all():
        return 'No data.'

    best_astronaut = Astronaut.objects \
        .annotate(num_of_missions=Count('mission_astronauts')) \
        .order_by('-num_of_missions', 'phone_number') \
        .first()

    if not best_astronaut:
        return 'No data.'

    return f"Top Astronaut: {best_astronaut.name} with {best_astronaut.num_of_missions} missions."


def get_top_commander():
    if not Astronaut.objects.all() or not Mission.objects.all():
        return 'No data.'

    best_commander = Astronaut.objects \
        .annotate(mission_count=Count('mission_commander')) \
        .order_by('-mission_count', 'phone_number') \
        .first()

    if best_commander.mission_count == 0:
        return 'No data.'

    return f"Top Commander: {best_commander.name} with {best_commander.mission_count} commanded missions."


