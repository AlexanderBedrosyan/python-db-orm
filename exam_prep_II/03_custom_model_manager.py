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


class CustomModelManager(models.Manager):

    def get_regular_customers(self):
        return self.annotate(total_orders=Count('order')).filter(total_orders__gt=2).order_by('-total_orders')


class Profile(CreationDate):
    full_name = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(2)]
    )
    email = models.EmailField()
    phone_number = models.CharField(
        max_length=15
    )
    address = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.full_name

    objects = CustomModelManager()