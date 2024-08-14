# mixins.py

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


class NameMixin(models.Model):
    name = models.CharField(
        max_length=80,
        validators=[MinLengthValidator(5)],
        unique=True
    )

    class Meta:
        abstract = True


class ModifiedAtMixin(models.Model):
    modified_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        abstract = True


# models.py
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


class Dragon(NameMixin, ModifiedAtMixin):

    class BreathChoices(models.TextChoices):
        FIRE = 'Fire', 'Fire'
        ICE = 'Ice', 'Ice'
        LIGHTNING = 'Lightning', 'Lightning'
        UNKNOWN = 'Unknown', 'Unknown'

    power = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[MinValueValidator(1.0), MaxValueValidator(10.0)],
        default=1.0
    )
    breath = models.CharField(
        max_length=9,
        choices=BreathChoices.choices,
        default=BreathChoices.UNKNOWN
    )
    is_healthy = models.BooleanField(
        default=True
    )
    birth_date = models.DateField(
        default=date.today
    )
    wins = models.PositiveSmallIntegerField(
        default=0
    )
    house = models.ForeignKey(
        to=House,
        on_delete=models.CASCADE,
        related_name='dragon_houses'
    )


class Quest(NameMixin, ModifiedAtMixin):
    code = models.CharField(
        max_length=4,
        validators=[
            RegexValidator(
                regex=r'^[A-Za-z#]{4}$',
            )
        ],
        unique=True
    )
    reward = models.FloatField(
        default=100.0
    )
    start_time = models.DateTimeField()
    dragons = models.ManyToManyField(
        to=Dragon,
        related_name='quest_dragons'
    )
    host = models.ForeignKey(
        to=House,
        on_delete=models.CASCADE,
        related_name='quest_house'
    )