from decimal import Decimal
from django.core import validators
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator, MinValueValidator, MaxValueValidator, \
    RegexValidator
from django.db import models
from datetime import date, datetime, timedelta
import re

# Create your models here.

from django.db import models
from django.db.models import QuerySet, Q, Count, Avg, Value, F
from .mixins import *


# get_authors_by_article_count()
# This method retrieves and returns all author objects, ordered by the number of articles each author has,
# descending, then by their emails ascending.


class TennisPlayer(models.Model):
    full_name = models.CharField(
        max_length=120,
        validators=[MinLengthValidator(5)]
    )
    birth_date = models.DateField()
    country = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(2)]
    )
    ranking = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(300)]
    )
    is_active = models.BooleanField(
        default=True
    )


class Tournament(models.Model):
    class SurfaceChoices(models.TextChoices):
        NOT_SELECTED = 'Not Selected', 'Not Selected'
        CLAY = 'Clay', 'Clay'
        GRASS = 'Grass', 'Grass'
        HARD_COURT = 'Hard Court', 'Hard Court'
    name = models.CharField(
        max_length=150,
        validators=[MinLengthValidator(2)],
        unique=True
    )
    location = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(2)]
    )
    prize_money = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    start_date = models.DateField()
    surface_type = models.CharField(
        max_length=12,
        choices=SurfaceChoices.choices,
        default=SurfaceChoices.NOT_SELECTED
    )


class Match(models.Model):
    class Meta:
        verbose_name_plural = 'Matches'

    score = models.CharField(
        max_length=100
    )
    summary = models.TextField(
        validators=[MinLengthValidator(5)]
    )
    date_played = models.DateTimeField()
    tournament = models.ForeignKey(
        to=Tournament,
        on_delete=models.CASCADE,
        related_name='match_tournament'
    )
    players = models.ManyToManyField(
        to=TennisPlayer,
        related_name='match_players'
    )
    winner = models.ForeignKey(
        to=TennisPlayer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='won_matches'
    )