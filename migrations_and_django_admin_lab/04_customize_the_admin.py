from django.contrib import admin
from main_app.models import Product #without main_app only for this file I mentioned it

# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'created_on')
    search_fields = ('name', 'category', 'supplier')
    list_filter = ('category', 'supplier')
    fieldsets = (
        (
            'General Information', {
                'fields': ('name', 'description', 'price', 'barcode')
            }
        ),
        (
            'Categorization', {
                'fields': ('category', 'supplier')
            }
        )
    )
    date_hierarchy = 'created_on'