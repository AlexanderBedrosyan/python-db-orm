# In caller.py
import os
import django
from datetime import date, datetime

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here

from main_app.models import *


def order_books_by_year():
    return '\n'.join([f"{curr_book.publication_year} year: {curr_book.title} by {curr_book.author}"
                      for curr_book in Book.objects.order_by('publication_year', 'title')])