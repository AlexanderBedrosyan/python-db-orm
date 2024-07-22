from django.core.exceptions import ValidationError
from decimal import Decimal
from django.core import validators
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator, MinValueValidator, MaxValueValidator, \
    RegexValidator
from django.db import models
from datetime import date, datetime, timedelta
import re
from main_app.validators import VideoGameValidator, release_year_checker

# Create your models here.

from django.db import models
from django.db.models import QuerySet, Q, Count, Avg



class VideoGameValidator:

    def __init__(self, min_rating: float, max_rating: float, message=None):
        self.min_rating = min_rating
        self.max_rating = max_rating
        self.message = message

    @property
    def message(self):
        return self.__message

    @message.setter
    def message(self, value):
        if value:
            self.__message = value
        else:
            self.__message = "The rating must be between 0.0 and 10.0"

    def __call__(self, value):
        if not (self.min_rating <= value <= self.max_rating):
            raise ValidationError(self.message)

    def deconstruct(self):
        return (
            f'main_app.validators.VideoGameValidator',  # Пътят към класа
            (self.min_rating, self.max_rating),  # Позиционните аргументи
            {'message': self.message},  # Ключовите аргументи
            {}  # Допълнителни опции
        )


def release_year_checker(value):
    if not (1990 <= value <= 2023):
        raise ValidationError("The release year must be between 1990 and 2023")


class VideoGameManager(models.Manager):

    def games_by_genre(self, genre: str):
        return self.filter(genre=genre)

    def recently_released_games(self, year: int):
        query = Q(release_year__gte=year)
        return self.filter(query)

    def highest_rated_game(self):
        return self.order_by('-rating').first()

    def lowest_rated_game(self):
        return self.order_by('rating').first()

    def average_rating(self):
        result = self.aggregate(avg_rating=Avg('rating'))
        return round(result['avg_rating'], 1)


class VideoGame(models.Model):
    GENRE_CHOICES = [
        ('Action', 'Action'),
        ('RPG', 'RPG'),
        ('Adventure', 'Adventure'),
        ('Sports', 'Sports'),
        ('Strategy', 'Strategy'),
    ]

    title = models.CharField(max_length=100)
    genre = models.CharField(max_length=100, choices=GENRE_CHOICES)
    release_year = models.PositiveIntegerField(validators=[release_year_checker])
    rating = models.DecimalField(max_digits=2,decimal_places=1,
                                 validators=[VideoGameValidator(0.0, 10.0)])

    objects = VideoGameManager()

    def __str__(self):
        return self.title