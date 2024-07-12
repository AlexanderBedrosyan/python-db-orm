# In models.py
from django.db import models
from datetime import date

# Create your models here.

class Animal(models.Model):
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=100)
    birth_date = models.DateField()
    sound = models.CharField(max_length=100)


class Employee(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=10)

    class Meta:
        abstract = True


class SpecialtiesChoices(models.TextField):
    MAMMALS = 'Mammals', 'Mammals'
    BIRDS = 'Birds', 'Birds'
    REPTILES = 'Reptiles', 'Reptiles'
    OTHERS = 'Others', 'Others'


class ZooKeeper(Employee):
    class SpecialtiesChoices(models.TextChoices):
        MAMMALS = 'Mammals', 'Mammals'
        BIRDS = 'Birds', 'Birds'
        REPTILES = 'Reptiles', 'Reptiles'
        OTHERS = 'Others', 'Others'

    specialty = models.CharField(max_length=10, choices=SpecialtiesChoices.choices)
    managed_animals = models.ManyToManyField(
        to=Animal
    )


class Veterinarian(Employee):
    license_number = models.CharField(max_length=10)