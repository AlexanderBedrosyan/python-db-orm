from django.core import validators
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models
from datetime import date, datetime, timedelta

# Create your models here.

from django.db import models



class CustomValidators:

    @staticmethod
    def validate_menu_categories(value):
        categories = ["Appetizers", "Main Course", "Desserts"]
        missing_categories = [category for category in categories if category not in value]
        if missing_categories:
            raise ValidationError('The menu must include each of the categories "Appetizers", "Main Course", "Desserts".')
        return value


class Menu(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(
        validators=[CustomValidators.validate_menu_categories]
    )
    restaurant = models.ForeignKey(
        to=Restaurant,
        on_delete=models.CASCADE
    )


class MenuReview(models.Model):
    reviewer_name = models.CharField(max_length=100)
    menu = models.ForeignKey(
        to=Menu,
        on_delete=models.CASCADE
    )
    review_content = models.TextField()
    rating = models.PositiveIntegerField(
        validators=[validators.MaxValueValidator(limit_value=5)]
    )

    class Meta:
        ordering = ['-rating']
        verbose_name = 'Menu Review'
        verbose_name_plural = 'Menu Reviews'
        unique_together = ['reviewer_name', 'menu']
        indexes = [
            models.Index(fields=['menu'], name="main_app_menu_review_menu_id")
        ]