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


# In caller.py

import os
from typing import List

import django
from datetime import date, datetime

from django.db.models import Case, When, F, Value, CharField

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import *


def show_all_authors_with_their_books():
    authors = Author.objects.all()
    details = [f"{author.name} has written - {', '.join([book.title for book in author.book_set.all()])}!"
               for author in authors if author.book_set.exists()]

    return '\n'.join(details)


def delete_all_authors_without_books():
    no_book_authors = Author.objects.all()

    for author in no_book_authors:
        if not author.book_set.all():
            author.delete()
