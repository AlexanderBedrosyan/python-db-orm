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


def get_last_completed_mission():
    query = Q(status='Completed')

    last_mission = Mission.objects \
        .filter(query) \
        .order_by('-launch_date') \
        .first()

    if not last_mission:
        return 'No data.'

    commander_name = None
    all_astronauts = last_mission.astronauts.all().order_by('name')
    spacecraft_name = last_mission.spacecraft.name
    total_space_walks = 0

    for a in all_astronauts:
        total_space_walks += a.spacewalks

    if not last_mission.commander:
        commander_name = 'TBA'
    else:
        commander_name = last_mission.commander.name

    return f"The last completed mission is: {last_mission.name}. Commander: {commander_name}. Astronauts: {', '.join(a.name for a in all_astronauts)}. Spacecraft: {spacecraft_name}. Total spacewalks: {total_space_walks}."


def get_most_used_spacecraft():
    if not Mission.objects.all():
        return 'No data.'

    spacecraft = Spacecraft.objects \
        .annotate(num_missions=Count('mission_spacecraft')) \
        .order_by('-num_missions', 'name') \
        .first()

    if not spacecraft:
        return 'No data.'

    unique_astronauts = []
    counter = 0
    for m in spacecraft.mission_spacecraft.all():
        for a in m.astronauts.all():
            if a not in unique_astronauts:
                unique_astronauts.append(a)
                counter += 1

    return f"The most used spacecraft is: {spacecraft.name}, manufactured by {spacecraft.manufacturer}, used in {spacecraft.num_missions} missions, astronauts on missions: {counter}."


def decrease_spacecrafts_weight():
    spacecrafts = Spacecraft.objects \
        .filter(mission_spacecraft__status='Planned', weight__gte=200.0)
    unique_spacecrafts = []
    for s in spacecrafts:
        if s not in unique_spacecrafts:
            unique_spacecrafts.append(s)

    counter = 0

    for spc in unique_spacecrafts:
        spc.weight -= 200
        spc.save()
        counter += 1

    if counter == 0:
        return f"No changes in weight."

    avg_weight = Spacecraft.objects.aggregate(avg=Avg('weight'))['avg']

    return f"The weight of {counter} spacecrafts has been decreased. The new average weight of all spacecrafts is {avg_weight:.1f}kg"
