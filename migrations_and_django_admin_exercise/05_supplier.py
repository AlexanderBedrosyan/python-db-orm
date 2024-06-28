from django.db import models
from datetime import date

# Create your models here.


class Supplier(models.Model):
    name = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, unique=True)
    address = models.TextField()

    def __str__(self):
        return f"{self.name} - {self.phone}"


from django.contrib import admin
from main_app.models import EventRegistration, Movie, Student, Supplier # it must be without main_app, it's added only for this py file

# Register your models here.


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone')
    list_filter = ('name', 'phone')
    search_fields = ('email', 'contact_person', 'phone')
    list_per_page = 20
    fieldsets = [
        (
            'Information',
            {
                'fields': ['name', 'contact_person', 'email', 'address']
            }
        )
    ]