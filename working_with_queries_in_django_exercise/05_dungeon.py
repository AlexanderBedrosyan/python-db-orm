# In caller.py

import os
from typing import List

import django
from datetime import date, datetime

from django.db.models import Case, When, F, Value, CharField

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here

from main_app.models import *



def show_hard_dungeons():
    ordered_dungeons = Dungeon.objects.filter(difficulty='Hard').order_by('-location')

    return '\n'.join([f'{dungeon.name} is guarded by {dungeon.boss_name} who has {dungeon.boss_health} health points!'
                      for dungeon in ordered_dungeons])


def bulk_create_dungeons(args: List[Dungeon]):
    Dungeon.objects.bulk_create(args)


def update_dungeon_names():
    Dungeon.objects.all().update(
        name=Case(
            When(difficulty='Easy', then=Value("The Erased Thombs")),
            When(difficulty='Medium', then=Value("The Coral Labyrinth")),
            When(difficulty='Hard', then=Value("The Lost Haunt"))
        )
    )


def update_dungeon_bosses_health():
    Dungeon.objects.exclude(difficulty='Easy').update(boss_health=500)


def update_dungeon_recommended_levels():
    Dungeon.objects.all().update(
        recommended_level=Case(
            When(difficulty='Easy', then=25),
            When(difficulty='Medium', then=50),
            When(difficulty='Hard', then=75)
        )
    )


def update_dungeon_rewards():
    Dungeon.objects.filter(
        boss_health=500
    ).update(reward="1000 Gold")

    Dungeon.objects.filter(
        location__startswith="E"
    ).update(reward="New dungeon unlocked")

    Dungeon.objects.filter(
        location__endswith="s"
    ).update(reward="Dragonheart Amulet")


def set_new_locations():
    Dungeon.objects.all().update(
        location=Case(
            When(recommended_level=25, then=Value("Enchanted Maze")),
            When(recommended_level=50, then=Value("Grimstone Mines")),
            When(recommended_level=75, then=Value("Shadowed Abyss")),
        )
    )
