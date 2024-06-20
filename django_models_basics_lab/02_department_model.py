from django.db import models


class Department(models.Model):
    class CityChoices(models.TextChoices):
        SOFIA = 'Sf', 'Sofia'
        PLOVDIV = 'Pd', 'Plovdiv'
        BURGAS = 'Bs', 'Burgas'
        VARNA = 'Vn', 'Varna'

    code = models.CharField(max_length=4, primary_key=True, unique=True)
    name = models.CharField(max_length=50, unique=True)
    employees_count = models.PositiveIntegerField(default=1, verbose_name='Employees Count')
    location = models.CharField(max_length=20, choices=CityChoices.choices)
    last_edited_on = models.DateTimeField(auto_now=True)