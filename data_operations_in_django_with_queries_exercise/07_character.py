# In models.py
from django.db import models
from datetime import date

# Create your models here.


class Character(models.Model):
    name = models.CharField(max_length=100)
    class_name = models.CharField(max_length=20, choices=ClassNameChoices.choices)
    level = models.PositiveIntegerField()
    strength = models.PositiveIntegerField()
    dexterity = models.PositiveIntegerField()
    intelligence = models.PositiveIntegerField()
    hit_points = models.PositiveIntegerField()
    inventory = models.TextField()

# In caller.py
import os
import django
from datetime import date, datetime

from django.db.models import Case, When, Value, F, CharField, PositiveIntegerField, TextField

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Pet, Artifact, Location, Car, Task, HotelRoom, Character


def update_characters():
    Character.objects.update(
        level=Case(
            When(class_name='Mage', then=F('level') + 3),
            default=F('level'),
            output_field=PositiveIntegerField()
        ),
        intelligence=Case(
            When(class_name='Mage', then=F('intelligence') - 7),
            default=F('intelligence'),
            output_field=PositiveIntegerField()
        ),
        hit_points=Case(
            When(class_name='Warrior', then=F('hit_points') / 2),
            default=('hit_points'),
            output_field=PositiveIntegerField()
        ),
        dexterity=Case(
            When(class_name='Warrior', then=F('dexterity') + 4),
            default=F('dexterity'),
            output_field=PositiveIntegerField()
        ),
        inventory=Case(
            When(class_name='Assassin', then=Value('The inventory is empty')),
            When(class_name='Scout', then=Value('The inventory is empty')),
            default=F('inventory'),
            output_field=TextField()
        )
    )


def fuse_characters(first_character: Character, second_character: Character):
    intelligence = (int(first_character.intelligence) + int(second_character.intelligence)) * 1.5
    inventory = ""
    if first_character.class_name in ['Mage', 'Scout']:
        inventory = "Bow of the Elven Lords, Amulet of Eternal Wisdom"
    elif first_character.class_name in ['Warrior', 'Assassin']:
        inventory = "Dragon Scale Armor, Excalibur"

    Character.objects.create(
        name=first_character.name + ' ' + second_character.name,
        class_name='Fusion',
        level=(int(first_character.level) + int(second_character.level)) // 2,
        strength=int((int(first_character.strength) + int(second_character.strength)) * 1.2),
        dexterity=int((int(first_character.dexterity) + int(second_character.dexterity)) * 1.4),
        intelligence=int(intelligence),
        hit_points=(int(first_character.hit_points) + int(second_character.hit_points)),
        inventory=inventory
    )

    first_character.delete()
    second_character.delete()


def grand_dexterity():
    Character.objects.all().update(dexterity=30)


def grand_intelligence():
    Character.objects.all().update(intelligence=40)


def grand_strength():
    Character.objects.all().update(strength=50)


def delete_characters():
    Character.objects.filter(inventory='The inventory is empty').delete()