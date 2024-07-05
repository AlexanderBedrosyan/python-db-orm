# In caller.py

import os
import django
from datetime import date, datetime

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here

from main_app.models import *


def filter_authors_by_birth_year(year_one, year_two):
    all_needed_authors = Author.objects.filter(birth_date__year__range=(year_one, year_two)).order_by('-birth_date')

    return '\n'.join([f"{author.birth_date}: {author.first_name} {author.last_name}" for author in all_needed_authors])

