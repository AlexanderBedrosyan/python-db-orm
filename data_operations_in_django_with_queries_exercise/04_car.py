# In models.py
from django.db import models
from datetime import date

# Create your models here.

class Car(models.Model):
    model = models.CharField(max_length=40)
    year = models.PositiveIntegerField()
    color = models.CharField(max_length=40)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    price_with_discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)


# In caller.py
import os
import django
from datetime import date, datetime

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Pet, Artifact, Location, Car


def apply_discount():
    all_cars = Car.objects.all()
    updated_car_discount = []

    for car in all_cars:
        if car.year == 2014:
            car.price_with_discount = car.price * 0.93
            updated_car_discount.append(car)
            continue

        car.price_with_discount = float(car.price) * ((100 - sum([int(ch) for ch in str(car.year)])) / 100)
        updated_car_discount.append(car)

    Car.objects.bulk_update(updated_car_discount, ['price_with_discount'])


def get_recent_cars():
    return Car.objects.filter(year__gt=2020).values('model', 'price_with_discount')


def delete_last_car():
    Car.objects.last().delete()