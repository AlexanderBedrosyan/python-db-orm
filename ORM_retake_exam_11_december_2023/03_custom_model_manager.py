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

class TennisManager(models.Manager):

    def get_tennis_players_by_wins_count(self):
        return self.annotate(win_num=Count('won_matches')).order_by('-win_num', 'full_name')


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

    objects = TennisManager()

    def __str__(self):
        return self.full_name