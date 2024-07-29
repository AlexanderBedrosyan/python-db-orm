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


def get_authors(search_name=None, search_email=None):
    if search_name is None and search_email is None:
        return ''

    query = None

    if search_name and search_email:
        query = Q(full_name__icontains=search_name) & Q(email__icontains=search_email)
    elif not search_name and search_email:
        query = Q(email__icontains=search_email)
    else:
        query = Q(full_name__icontains=search_name)

    author = Author.objects.filter(query).order_by('-full_name')

    if not author:
        return ''

    information = []

    for a in author:
        status = 'Banned' if a.is_banned else 'Not Banned'
        information.append(f"Author: {a.full_name}, email: {a.email}, status: {status}")

    return '\n'.join(information)


def get_top_publisher():
    top_publisher = Author.objects \
                     .annotate(num_articles=Count('article_authors')) \
                     .order_by('-num_articles', 'email') \
                     .first()

    if not Article.objects.all() or not top_publisher:
        return ''

    return f"Top Author: {top_publisher.full_name} with {top_publisher.num_articles} published articles."


def get_top_reviewer():
    top_reviewer = Author.objects \
        .annotate(num_reviews=Count('review_author')) \
        .order_by('-num_reviews', 'email') \
        .first()

    if not Review.objects.all() or not top_reviewer:
        return ''

    return f"Top Reviewer: {top_reviewer.full_name} with {top_reviewer.num_reviews} published reviews."