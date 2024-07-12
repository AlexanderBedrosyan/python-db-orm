# In models.py
from django.db import models
from datetime import date

# Create your models here.

class Driver(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)


class DrivingLicense(models.Model):
    license_number = models.CharField(max_length=10, unique=True)
    issue_date = models.DateField()
    driver = models.OneToOneField(
        to=Driver,
        on_delete=models.CASCADE,
        related_name='license'
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


def calculate_licenses_expiration_dates():
    licenses = DrivingLicense.objects.all().order_by('-license_number')
    information = []
    for license in licenses:
        expiration_date = license.issue_date + timedelta(days=365)
        information.append(f'License with number: {license.license_number} expires on {expiration_date}!')

    return '\n'.join(information)


def get_drivers_with_expired_licenses(due_date: date):
    drivers = Driver.objects.all()
    results = []

    for driver in drivers:
        if (driver.license.issue_date + timedelta(days=365)) > due_date:
            results.append(driver)

    return results
