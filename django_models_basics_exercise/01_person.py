from django.db import models
from datetime import date

# Create your models here.


class Person(models.Model):
    name = models.CharField(max_length=30)
    age = models.PositiveIntegerField()