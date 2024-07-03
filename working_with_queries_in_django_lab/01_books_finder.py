# In caller.py

import os
import django
from datetime import date, datetime

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here

from main_app.models import *


def find_books_by_genre_and_language(book_genre: str, book_language: str):
    return Book.objects.filter(genre=book_genre, language=book_language)
