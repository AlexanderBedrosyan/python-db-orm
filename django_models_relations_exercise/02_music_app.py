# In models.py
from django.db import models
from datetime import date

# Create your models here.


class Author(models.Model):
    name = models.CharField(max_length=40)


class Book(models.Model):
    title = models.CharField(max_length=40)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    author = models.ForeignKey(
        to=Author,
        on_delete=models.CASCADE
    )


class Song(models.Model):
    title = models.CharField(max_length=100, unique=True)


class Artist(models.Model):
    name = models.CharField(max_length=100, unique=True)
    songs = models.ManyToManyField(
        to=Song,
        related_name='artists'
    )


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


def add_song_to_artist(artist_name: str, song_title: str):
    artist = Artist.objects.get(name=artist_name)
    song = Song.objects.get(title=song_title)
    artist.songs.add(song)


def get_songs_by_artist(artist_name):
    return Artist.objects.get(name=artist_name).songs.all().order_by('-id')


def remove_song_from_artist(artist_name: str, song_title:str):
    artist = Artist.objects.get(name=artist_name)
    song = Song.objects.get(title=song_title)
    song.artists.remove(artist)

