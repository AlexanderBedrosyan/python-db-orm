import os
from typing import List

import django
from datetime import date, datetime, timedelta

from django.db.models import Case, When, F, Value, CharField, Avg, QuerySet, Count, Sum, Q

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import *


def filter_products():
    query_needed = Q(price__gt=3) & Q(is_available=True)
    products = Product.objects.filter(query_needed).order_by('-price', 'name')
    information = []

    for curr_product in products:
        information.append(f"{curr_product.name}: {curr_product.price}lv.")
    return '\n'.join(information)