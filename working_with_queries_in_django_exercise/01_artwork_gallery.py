# In models.py
from django.db import models
from datetime import date

# Create your models here.


class ArtworkGallery(models.Model):
    artist_name = models.CharField(max_length=100)
    art_name = models.CharField(max_length=100)
    rating = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)


# In caller.py
import os
import django
from datetime import date, datetime

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here

from main_app.models import *


def show_highest_rated_art():
    needed_art = ArtworkGallery.objects.order_by('-rating', 'id').first()
    return f"{needed_art.art_name} is the highest-rated art with a {needed_art.rating} rating!"


def bulk_create_arts(first_art: ArtworkGallery, second_art: ArtworkGallery):
    ArtworkGallery.objects.bulk_create([first_art, second_art])


def delete_negative_rated_arts():
    ArtworkGallery.objects.filter(rating__lt=0).delete()

