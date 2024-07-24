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
from django.db.models import QuerySet, Q, Count, Avg, Value, F


class Exercise(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    difficulty_level = models.PositiveIntegerField()
    duration_minutes = models.PositiveIntegerField()
    repetitions = models.PositiveIntegerField()

    @classmethod
    def get_long_and_hard_exercises(cls):
        query = Q(duration_minutes__gt=30) & Q(difficulty_level__gte=10)
        return cls.objects.filter(query)

    @classmethod
    def get_short_and_easy_exercises(cls):
        query = Q(duration_minutes__lt=15) & Q(difficulty_level__lt=5)
        return cls.objects.filter(query)

    @classmethod
    def get_exercises_within_duration(cls, min_duration: int, max_duration: int):
        query = Q(duration_minutes__gte=min_duration) & Q(duration_minutes__lte=max_duration)
        return cls.objects.filter(query)

    @classmethod
    def get_exercises_with_difficulty_and_repetitions(cls, min_difficulty: int, min_repetitions: int):
        query = Q(difficulty_level__gte=min_difficulty) & Q(repetitions__gte=min_repetitions)
        return cls.objects.filter(query)