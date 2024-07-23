from decimal import Decimal
from django.core import validators
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator, MinValueValidator, MaxValueValidator, \
    RegexValidator
from django.db import models
from datetime import date, datetime, timedelta
import re
from main_app.validators import VideoGameValidator, release_year_checker

# Create your models here.

from django.db import models
from django.db.models import QuerySet, Q, Count, Avg, Value, F


class Task(models.Model):
    PRIORITIES = (
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High')
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    priority = models.CharField(max_length=20, choices=PRIORITIES)
    is_completed = models.BooleanField(default=False)
    creation_date = models.DateField()
    completion_date = models.DateField()

    @classmethod
    def ongoing_high_priority_tasks(cls):
        query = Q(priority='High') & Q(is_completed=False) & Q(completion_date__gt=F('creation_date'))
        return cls.objects.filter(query)

    @classmethod
    def completed_mid_priority_tasks(cls):
        query = Q(priority='Medium') & Q(is_completed=True)
        return cls.objects.filter(query)

    @classmethod
    def search_tasks(cls, query: str):
        query = Q(description__icontains=query) | Q(title__icontains=query)
        return cls.objects.filter(query)

    @classmethod
    def recent_completed_tasks(cls, days: int):
        query = Q(completion_date__gte=F('creation_date') - timedelta(days)) & Q(is_completed=True)
        return cls.objects.filter(query)