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


class CustomManager(models.Manager):

    def get_directors_by_movies_count(self):
        return self.annotate(movie_count=Count('movie')).order_by('-movie_count', 'full_name')
