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


# class AstronautManager(models.Manager):
#     def get_astronauts_by_missions_count(self):
#         return self.annotate(num_of_missions=Count('mission_astronauts')).order_by('-num_of_missions', 'phone_number')

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

    # objects = AstronautManager()

    def __str__(self):
        return self.name


class Spacecraft(NameMixin, LaunchDateMixin, UpdateMixin):
    manufacturer = models.CharField(
        max_length=120
    )
    capacity = models.SmallIntegerField(
        validators=[MinValueValidator(1)]
    )
    weight = models.FloatField(
        validators=[MinValueValidator(0.0)]
    )

    def __str__(self):
        return self.name




class Mission(NameMixin, LaunchDateMixin, UpdateMixin):
    class StatusChoices(models.TextChoices):
        PLANNED = 'Planned', 'Planned'
        ONGOING = 'Ongoing', 'Ongoing'
        COMPLETED = 'Completed', 'Completed'
    description = models.TextField(
        blank=True,
        null=True
    )
    status = models.CharField(
        max_length=9,
        choices=StatusChoices.choices,
        default=StatusChoices.PLANNED
    )
    spacecraft = models.ForeignKey(
        to=Spacecraft,
        on_delete=models.CASCADE,
        related_name='mission_spacecraft'
    )
    astronauts = models.ManyToManyField(
        to=Astronaut,
        related_name='mission_astronauts'
    )
    commander = models.ForeignKey(
        to=Astronaut,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='mission_commander'
    )

    def __str__(self):
        return self.name
