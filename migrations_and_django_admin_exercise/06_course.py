from django.db import models
from datetime import date

# Create your models here.


class Course(models.Model):
    title = models.CharField(max_length=90)
    lecturer = models.CharField(max_length=90)
    description = models.TextField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField(auto_now=True)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} - {self.lecturer}"


from django.contrib import admin
from main_app.models import EventRegistration, Movie, Student, Supplier, Course # it must be without main_app, it's added only for this py file

# Register your models here.

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'lecturer', 'price', 'start_date')
    list_filter = ('is_published', 'lecturer')
    search_fields = ('title', 'lecturer')
    readonly_fields = ['start_date']
    fieldsets = [
        (
            'Course Information',
            {
                'fields': ['title', 'lecturer', 'price', 'start_date', 'is_published']
            }
        ),
        (
            'Description',
            {
                'fields': ['description']
            }
        )
    ]