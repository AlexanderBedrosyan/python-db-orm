# In caller.py
import os
import django
from datetime import date, datetime

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here

from main_app.models import *


def filter_authors_by_nationalities(current_nationality):
    all_needed_authors = Author.objects.filter(nationality=current_nationality).order_by('first_name', 'last_name')

    information = []

    for author in all_needed_authors:
        if author.biography is None:
            information.append(f"{author.first_name} {author.last_name}")
            continue
        information.append(f"{author.biography}")

    return '\n'.join(information)