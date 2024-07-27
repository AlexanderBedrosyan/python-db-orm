import os
from typing import List

import django
from datetime import date, datetime, timedelta

from django.db.models import Case, When, F, Value, CharField, Avg, QuerySet, Count, Sum, Q, Max

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import *


def get_top_products():
    products = Product.objects.annotate(total_amount=Count('all_products')).filter(total_amount__gt=0).order_by('-total_amount', 'name')[0:5]

    if not Order.objects.all() or not products:
        return ""

    information = ['Top products:']

    for p in products:
        information.append(
            f'{p.name}, sold {p.total_amount} times'
        )

    return '\n'.join(information)


def apply_discounts():
    orders = Order.objects.annotate(all_products=Count('products')).filter(all_products__gt=2, is_completed=False)

    updated_orders = []

    for o in orders:
        o.total_price = o.total_price * Decimal(0.90)
        updated_orders.append(o)

    if updated_orders:
        Order.objects.bulk_update(updated_orders, ['total_price'])

    return f"Discount applied to {len(updated_orders)} orders."


def complete_order():
    order = Order.objects.filter(is_completed=False).order_by('id').first()

    if not Order.objects.all() or not order:
        return ''

    for product in order.products.all():
        product.in_stock -= 1

        if product.in_stock == 0:
            product.is_available = False

        product.save()

    order.is_completed = True
    order.save()

    return 'Order has been completed!'
