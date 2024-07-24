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


class Person(models.Model):
    full_name = models.CharField(
        max_length=120,
        validators=[MinLengthValidator(2)]
    )
    birth_date = models.DateField(
        default='1900-01-01'
    )
    nationality = models.CharField(
        max_length=50,
        default='Unknown'
    )

    class Meta:
        abstract = True


class Director(Person):
    years_of_experience = models.SmallIntegerField(
        validators=[MinValueValidator(0)],
        default=0
    )


class Actor(Person):
    is_awarded = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now=True)


class GenreChoices(models.TextChoices):
    ACTION = 'Action', 'Action'
    COMEDY = 'Comedy', 'Comedy'
    DRAMA = 'Drama', 'Drama'
    OTHER = 'Other', 'Other'


class Movie(models.Model):
    title = models.CharField(
        max_length=150,
        validators=[MinLengthValidator(5)]
    )
    release_date = models.DateField()
    storyline = models.TextField(blank=True, null=True)
    genre = models.CharField(
        max_length=6,
        choices=GenreChoices.choices,
        default='Other'
    )
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)],
        default=0.0
    )
    is_classic = models.BooleanField(default=False)
    is_awarded = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now=True)
    director = models.ForeignKey(
        to=Director,
        on_delete=models.CASCADE
    )
    starring_actor = models.ForeignKey(
        to=Actor,
        blank=True, null=True,
        on_delete=models.SET_NULL,
        related_name='starring_movies'
    )
    actors = models.ManyToManyField(
        to=Actor,
        related_name='movies'
    )