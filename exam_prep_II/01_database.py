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


class CreationDate(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

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



class Product(CreationDate):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    in_stock = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Order(CreationDate):
    profile = models.ForeignKey(
        to=Profile,
        on_delete=models.CASCADE
    )
    products = models.ManyToManyField(
        to=Product,
        related_name='all_products'
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    is_completed = models.BooleanField(default=False)