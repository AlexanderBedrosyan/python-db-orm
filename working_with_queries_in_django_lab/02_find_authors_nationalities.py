# In caller.py
import os
import django
from datetime import date, datetime

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here

from main_app.models import *


def find_authors_nationalities():
    return '\n'.join([f"{curr_author.first_name} {curr_author.last_name} is {curr_author.nationality}"
                      for curr_author in Author.objects.filter(nationality__isnull=False)])