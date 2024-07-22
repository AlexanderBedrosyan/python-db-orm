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


def ordered_products_per_customer():
    prefetched_orders = Order.objects.prefetch_related('orderproduct_set__product__category').order_by('id')
    result = []
    for order in prefetched_orders:
        result.append(f"Order ID: {order.id}, Customer: {order.customer.username}")
        for order_product in order.orderproduct_set.all():
            result.append(f"- Product: {order_product.product.name}, Category: {order_product.product.category.name}")
    return "\n".join(result)
