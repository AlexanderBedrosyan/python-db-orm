# In models.py
from django.db import models
from datetime import date

# Create your models here.


class Author(models.Model):
    name = models.CharField(max_length=40)


class Book(models.Model):
    title = models.CharField(max_length=40)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    author = models.ForeignKey(
        to=Author,
        on_delete=models.CASCADE
    )


class Song(models.Model):
    title = models.CharField(max_length=100, unique=True)


class Artist(models.Model):
    name = models.CharField(max_length=100, unique=True)
    songs = models.ManyToManyField(
        to=Song,
        related_name='artists'
    )


class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)


class Review(models.Model):
    description = models.TextField(max_length=200)
    rating = models.PositiveSmallIntegerField()
    product = models.ForeignKey(
        to=Product,
        on_delete=models.CASCADE,
        related_name='reviews'
    )


# In caller.py

import os
from typing import List

import django
from datetime import date, datetime

from django.db.models import Case, When, F, Value, CharField, Avg, QuerySet

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import *


def calculate_average_rating_for_product_by_name(product_name: str):
    product = Product.objects.get(name=product_name)
    return product.reviews.aggregate(average_rating=Avg('rating'))['average_rating']


def get_reviews_with_high_ratings(threshold: int):
    review = Review.objects.filter(rating__gte=threshold)
    return review


def get_products_with_no_reviews():
    products_without_reviews = Product.objects.annotate(num_reviews=models.Count('reviews')).filter(num_reviews=0).order_by('-name')
    return products_without_reviews


def delete_products_without_reviews():
    no_review_products = get_products_with_no_reviews()
    for prd in no_review_products:
        prd.delete()

