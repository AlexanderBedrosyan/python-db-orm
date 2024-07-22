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


def give_discount():
    query_needed = Q(price__gt=3) & Q(is_available=True)
    query_available_products = Q(is_available=True)
    Product.objects.filter(query_needed).update(price=F('price') * 0.70)
    products = Product.objects.filter(query_available_products).order_by('-price', 'name')
    information = []

    for product in products:
        information.append(f'{product.name}: {product.price}lv.')

    return '\n'.join(information)
