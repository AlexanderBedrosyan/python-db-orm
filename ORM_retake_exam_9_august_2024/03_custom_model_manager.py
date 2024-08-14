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


class HosesManager(models.Manager):
    def get_houses_by_dragons_count(self):
        return self.annotate(count_dragons=Count('dragon_houses')).order_by('-count_dragons', 'name')

class House(NameMixin, ModifiedAtMixin):
    motto = models.TextField(
        blank=True,
        null=True
    )
    is_ruling = models.BooleanField(
        default=False
    )
    castle = models.CharField(
        max_length=80,
        blank=True,
        null=True
    )
    wins = models.PositiveSmallIntegerField(
        default=0
    )

    objects = HosesManager()

    def __str__(self):
        return self.name