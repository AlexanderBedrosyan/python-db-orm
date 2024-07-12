# In models.py

from django.db import models
from datetime import date

# Create your models here.


class Owner(models.Model):
    name = models.CharField(max_length=50)


class Car(models.Model):
    model = models.CharField(max_length=50)
    year = models.PositiveIntegerField()
    owner = models.ForeignKey(
        to=Owner,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='cars'
    )


class Registration(models.Model):
    registration_number = models.CharField(max_length=10)
    registration_date = models.DateField(blank=True, null=True)
    car = models.OneToOneField(
        to=Car,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='registration'
    )

# In caller.py

import os
from typing import List

import django
from datetime import date, datetime, timedelta

from django.db.models import Case, When, F, Value, CharField, Avg, QuerySet

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import *


def register_car_by_owner(owner: Owner):
    first_registration = Registration.objects.filter(car_id__isnull=True).first()
    first_car = Car.objects.filter(owner_id__isnull=True).first()

    first_registration.registration_date = date.today()
    first_registration.car_id = first_car.id
    first_car.owner_id = owner.id

    first_registration.save()
    first_car.save()

    return f"Successfully registered {first_car.model} to {owner.name} with registration number {first_registration.registration_number}."
