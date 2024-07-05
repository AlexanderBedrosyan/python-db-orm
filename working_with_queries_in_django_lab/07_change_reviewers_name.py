# In caller.py
import os
import django
from datetime import date, datetime

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here

from main_app.models import *


def change_reviewer_name(old_name, new_name):
    Review.objects.filter(reviewer_name=old_name).update(reviewer_name=new_name)

    return Review.objects.all()
