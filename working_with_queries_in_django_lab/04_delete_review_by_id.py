# In caller.py

import os
import django
from datetime import date, datetime

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here

from main_app.models import *


def delete_review_by_id(review_id):
    needed_review = Review.objects.get(pk=review_id)
    needed_review.delete()

    return f"Review by {needed_review.reviewer_name} was deleted"
