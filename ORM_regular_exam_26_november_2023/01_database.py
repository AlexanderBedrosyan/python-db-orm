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


class ContentMixin(models.Model):
    content = models.TextField(
        validators=[MinLengthValidator(10)]
    )

    class Meta:
        abstract = True


class PublishedOnMixin(models.Model):
    published_on = models.DateTimeField(
       auto_now_add=True,
       editable=False
    )

    class Meta:
        abstract = True


class Author(models.Model):

    full_name = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(3)]
    )
    email = models.EmailField(unique=True)
    is_banned = models.BooleanField(default=False)
    birth_year = models.PositiveIntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(2005)]
    )
    website = models.URLField(blank=True, null=True)


class Article(ContentMixin, PublishedOnMixin):
    class CategoryChoices(models.TextChoices):
        TECHNOLOGY = 'Technology', 'Technology'
        SCIENCE = 'Science', 'Science'
        EDUCATION = 'Education', 'Education'

    title = models.CharField(
        max_length=200,
        validators=[MinLengthValidator(5)]
    )
    category = models.CharField(
        max_length=10,
        choices=CategoryChoices.choices,
        default='Technology'
    )
    authors = models.ManyToManyField(
        to=Author,
        related_name='article_authors'
    )


class Review(PublishedOnMixin, ContentMixin):
    rating = models.FloatField(
        validators=[MinValueValidator(1.0), MaxValueValidator(5.0)]
    )
    author = models.ForeignKey(
        to=Author,
        related_name='review_author',
        on_delete=models.CASCADE
    )
    article = models.ForeignKey(
        to=Article,
        related_name='review_article',
        on_delete=models.CASCADE
    )