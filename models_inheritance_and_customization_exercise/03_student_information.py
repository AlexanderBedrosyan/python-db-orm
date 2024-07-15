from django.core.exceptions import ValidationError
from django.db import models
from datetime import date

# Create your models here.

from django.db import models


class StudentIDField(models.PositiveIntegerField):
    def get_prep_value(self, value):

        try:
            value = int(value)
        except (TypeError, ValueError):
            raise ValueError("Invalid input for student ID")

        if value <= 0:
            raise ValidationError("ID cannot be less than or equal to zero")

        return value

    def clean(self, value, model_instance):
        value = self.get_prep_value(value)
        return super().clean(value, model_instance)


class Student(models.Model):
    name = models.CharField(max_length=100)
    student_id = StudentIDField()

    def __str__(self):
        return f"{self.name} ({self.student_id})"
