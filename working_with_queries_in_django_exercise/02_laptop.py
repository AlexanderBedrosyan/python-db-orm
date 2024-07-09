# In models.py
from django.db import models
from datetime import date

# Create your models here.


class LaptopModelChoices(models.TextChoices):
    ASUS = 'Asus', 'Asus'
    APPLE = 'Apple', 'Apple'
    LENOVO = 'Lenovo', 'Lenovo'
    DELL = 'Dell', 'Dell'
    ACER = 'Acer', 'Acer'


class OperationSystemChoices(models.TextChoices):
    WINDOWS = 'Windows', 'Windows'
    MACOS = 'MacOS', 'MacOS'
    LINUX = 'Linux', 'Linux'
    CHROME_OS = 'Chrome OS', 'Chrome OS'


class Laptop(models.Model):
    brand = models.CharField(max_length=20, choices=LaptopModelChoices.choices)
    processor = models.CharField(max_length=100)
    memory = models.PositiveIntegerField(help_text='Memory in GB')
    storage = models.PositiveIntegerField(help_text='Storage in GB')
    operation_system = models.CharField(choices=OperationSystemChoices.choices)
    price = models.DecimalField(max_digits=10, decimal_places=2)


# In caller.py
import os
from typing import List

import django
from datetime import date, datetime

from django.db.models import Case, When, F, Value

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here

from main_app.models import *


def show_the_most_expensive_laptop():
    most_expensive_laptop = Laptop.objects.order_by('-price', '-id').first()
    return f"{most_expensive_laptop.brand} is the most expensive laptop available for {most_expensive_laptop.price}$!"


def bulk_create_laptops(args: List[Laptop]):
    Laptop.objects.bulk_create(args)


def update_to_512_GB_storage():
    Laptop.objects.filter(brand__in=('Asus', 'Lenovo')).update(storage=512)


def update_to_16_GB_memory():
    Laptop.objects.filter(brand__in=('Apple', 'Dell', 'Acer')).update(memory=16)


def update_operation_systems():
    Laptop.objects.update(
        operation_system=Case(
            When(brand='Asus', then=Value('Windows')),
            When(brand='Apple', then=Value('MacOS')),
            When(brand__in=('Dell', 'Acer'), then=Value('Linux')),
            When(brand='Lenovo', then=Value('Chrome OS'))
        )
    )


def delete_inexpensive_laptops():
    Laptop.objects.filter(price__lt=1200).delete()
