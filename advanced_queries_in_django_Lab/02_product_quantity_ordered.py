import os
from typing import List

import django
from datetime import date, datetime, timedelta

from django.db.models import Case, When, F, Value, CharField, Avg, QuerySet, Count, Sum

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import *


def product_quantity_ordered():
    orders = (Order.objects.values('orderproduct__product__name')
            .annotate(total_amount=Sum('orderproduct__quantity'), product_name=F('orderproduct__product__name'))
            .exclude(total_amount__lte=0)
            .order_by('-total_amount'))
    result = []
    for ord in orders:
        result.append(f"Quantity ordered of {ord['product_name']}: {ord['total_amount']}")
    return '\n'.join(result)
