from django.core import validators
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models
from datetime import date, datetime, timedelta

# Create your models here.

from django.db import models


class Restaurant(models.Model):
    name = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(2, message="Name must be at least 2 characters long."),
            MaxLengthValidator(100, message="Name cannot exceed 100 characters.")
        ]
    )
    location = models.CharField(
        max_length=200,
        validators=[
            MinLengthValidator(2, message="Location must be at least 2 characters long."),
            MaxLengthValidator(200, message="Location cannot exceed 200 characters.")
        ]
    )
    description = models.TextField(
        blank=True,
        null=True
    )
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        validators=[
            MinValueValidator(0.00, message="Rating must be at least 0.00."),
            MaxValueValidator(5.00, message="Rating cannot exceed 5.00.")
        ]
    )


class RestaurantReview(models.Model):
    reviewer_name = models.CharField(max_length=100)
    restaurant = models.ForeignKey(
        to=Restaurant,
        on_delete=models.CASCADE
    )
    review_content = models.TextField()
    rating = models.PositiveIntegerField(
        validators=[validators.MaxValueValidator(limit_value=5)]
    )

    class Meta:
        ordering = ['-rating']
        verbose_name = 'Restaurant Review'
        verbose_name_plural = 'Restaurant Reviews'
        unique_together = ['reviewer_name', 'restaurant']
