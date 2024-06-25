from django.contrib import admin
from main_app.models import Product #without main_app only for this file I mentioned it

# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass