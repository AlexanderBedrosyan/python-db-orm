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


def get_profiles(search_string=None):

    if search_string is None: # Да попитам, защо с if not search_string не работи правилно.
        return ""

    profiles = Profile.objects.annotate(total_orders=Count('order'))\
        .filter(Q(full_name__icontains=search_string) | Q(email__icontains=search_string) | Q(phone_number__icontains=search_string)
    ).order_by('full_name')

    if not profiles:
        return ""

    final_result = []
    for profile in profiles:
        final_result.append(f"Profile: {profile.full_name}, "
                            f"email: {profile.email}, "
                            f"phone number: {profile.phone_number}, "
                            f"orders: {profile.total_orders}")

    return '\n'.join(final_result)


def get_loyal_profiles():
    query = Q(total_orders__gt=2)

    profiles = Profile.objects.annotate(total_orders=Count('order')).filter(query).order_by('-total_orders')

    if not profiles:
        return ''

    information = [f'Profile: {p.full_name}, orders: {p.total_orders}' for p in profiles]

    return '\n'.join(information)


def get_last_sold_products():
    if not Order.objects.all():
        return ''

    order = Order.objects.all().order_by('-id').first()

    return f"Last sold products: {', '.join([pr.name for pr in order.products.all()])}"