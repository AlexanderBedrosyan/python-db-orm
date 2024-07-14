# In models.py

from django.core.exceptions import ValidationError
from django.db import models
from datetime import date

# Create your models here.

class Animal(models.Model):
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=100)
    birth_date = models.DateField()
    sound = models.CharField(max_length=100)

    @property
    def age(self):
        return (date.today() - self.birth_date).days // 365