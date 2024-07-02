# In models.py
from django.db import models
from datetime import date

# Create your models here.


class Pet(models.Model):
    name = models.CharField(max_length=40)
    species = models.CharField(max_length=40)


# In caller.py
import os
import django
from datetime import date, datetime

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Pet


def create_pet(name:str, species: str) -> str:
    Pet.objects.bulk_create([Pet(
        name=name,
        species=species
    )])

    return f"{name} is a very cute {species}!"