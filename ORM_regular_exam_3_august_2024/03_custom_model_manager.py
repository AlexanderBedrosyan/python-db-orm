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


class AstronautManager(models.Manager):
    def get_astronauts_by_missions_count(self):
        return self.annotate(num_of_missions=Count('mission_astronauts')).order_by('-num_of_missions', 'phone_number')

class Astronaut(NameMixin, UpdateMixin):
    phone_number = models.CharField(
        max_length=15,
        validators=[RegexValidator(r'^\d+$')],
        unique=True
    )
    is_active = models.BooleanField(
        default=True
    )
    date_of_birth = models.DateField(
        blank=True,
        null=True
    )
    spacewalks = models.IntegerField(
        validators=[MinValueValidator(0)],
        default=0
    )

    objects = AstronautManager()

    def __str__(self):
        return self.name

