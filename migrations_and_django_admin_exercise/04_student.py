from django.db import models
from datetime import date

# Create your models here.


class Student(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.PositiveIntegerField()
    grade = models.CharField(max_length=10)
    date_of_birth = models.DateField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


from django.contrib import admin
from main_app.models import EventRegistration, Movie, Student # it must be without main_app, it's added only for this py file

# Register your models here.


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'age', 'grade')
    list_filter = ('age', 'grade', 'date_of_birth')
    search_fields = ('first_name',)
    fieldsets = [
        (
            'Personal Information',
            {
                'fields': ['first_name', 'last_name', 'age', 'date_of_birth']
            },
        ),
        (
            'Academic Information',
            {
                'fields': ['grade']
            },
        ),
    ]