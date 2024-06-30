from django.db import models
from datetime import date

# Create your models here.

class Smartphone(models.Model):
    brand = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    category = models.CharField(max_length=20, default='No category')

# After migration of Smartphone model create an empty migration and add the code below
# Generated by Django 4.2 on 2024-06-28 21:17

from django.db import migrations

# •	The second one generates a new value - "Expensive" to the category field only if the price is greater
# than or equal to 750. Otherwise, the new value should be "Cheap".


def update_price(apps, schema_editor):
    smartphone = apps.get_model('main_app', 'smartphone')
    all_smartphones = smartphone.objects.all()

    updated_smartphones = []

    for curr_smartphone in all_smartphones:
        curr_smartphone.price = len(curr_smartphone.brand) * 120
        updated_smartphones.append(curr_smartphone)

    smartphone.objects.bulk_update(updated_smartphones, ['price'])


def return_correct_category(num):
    if num >= 750:
        return 'Expensive'
    else:
        return 'Cheap'


def update_category(apps, schema_editor):
    smartphone = apps.get_model('main_app', 'smartphone')
    all_smartphones = smartphone.objects.all()

    updated_smartphones = []

    for curr_smartphone in all_smartphones:
        curr_smartphone.category = return_correct_category(float(curr_smartphone.price))
        updated_smartphones.append(curr_smartphone)

    smartphone.objects.bulk_update(updated_smartphones, ['category'])


def reverse_fulling_of_columns_category_and_price(apps, schema_editor):
    smartphone_model = apps.get_model("main_app", "SmartPhone")

    for smartphone in smartphone_model.objects.all():
        smartphone.category = smartphone_model._meta.get_field('category').default
        smartphone.price = smartphone_model._meta.get_field('price').default
        smartphone.save()


def set_all_columns(apps, schema_editor):
    update_price(apps, schema_editor)
    update_category(apps, schema_editor)


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0013_smartphone'),
    ]

    operations = [
        migrations.RunPython(set_all_columns, reverse_fulling_of_columns_category_and_price)
    ]