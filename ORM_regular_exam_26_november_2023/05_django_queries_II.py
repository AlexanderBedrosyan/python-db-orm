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


def get_latest_article():
    last_article = Article.objects \
                    .annotate(num_reviews=Count('review_article'), avg_rating=Avg('review_article__rating')) \
                    .order_by('-published_on') \
                    .first()

    if not last_article:
        return ''

    authors = [a.full_name for a in last_article.authors.all().order_by('full_name')]

    avg_rating = f"{last_article.avg_rating:.2f}" if last_article.avg_rating is not None else f"{0:.2f}"

    return f"The latest article is: {last_article.title}. Authors: {', '.join(authors)}. Reviewed: {last_article.num_reviews} times. Average Rating: {avg_rating}."


def get_top_rated_article():
    if not Article.objects.all():
        return ''

    if not Review.objects.all():
        return ''

    top_article = Article.objects \
        .annotate(avg_rating=Avg('review_article__rating'), num_reviews=Count('review_article__id')) \
        .order_by('-avg_rating', 'title') \
        .first()

    if not top_article:
        return ''

    return f"The top-rated article is: {top_article.title}, with an average rating of {top_article.avg_rating:.2f}, reviewed {top_article.num_reviews} times."


def ban_author(email=None):
    if email is None:
        return f"No authors banned."

    if not Author.objects.all():
        return "No authors banned."

    author = Author.objects.filter(email=email)

    if not author:
        return f"No authors banned."

    author.update(is_banned=True)

    all_reviews = author[0].review_author.all()
    count_reviews = 0

    for rev in all_reviews:
        count_reviews += 1
        rev.delete()

    return f"Author: {author[0].full_name} is banned! {count_reviews} reviews deleted."
