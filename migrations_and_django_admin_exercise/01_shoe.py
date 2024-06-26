# Create model Shoe

from django.db import models
from datetime import date

# Create your models here.


class Shoe(models.Model):
    brand = models.CharField(max_length=25)
    size = models.PositiveIntegerField()

# Migrate the mode Shoe - makemigrations, migrate

# Check list of migrations:
# python manage.py showmigrations

# python manage.py sqlmigrate main_app 0001_initial - this shows the SQL code behind the migration in our case:
# CREATE TABLE "main_app_shoe" ("id" bigint NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY, "brand" varchar(25)
# NOT NULL, "size" integer NOT NULL CHECK ("size" >= 0));
# COMMIT;

# Create a new model:

class UniqueBrands(models.Model):
    brand_name = models.CharField(max_length=25, unique=True)

# Only makemigrations in terminal
# Then create an empty migration with name migrate_unique_brands
# python manage.py makemigrations main_app --name migrate_unique_brands --empty
# Fill the new migration file with the below code

# Generated by Django 4.2 on 2024-06-23 13:16

from django.db import migrations


def create_unique_brands(apps, scheme_editor):
    shoe = apps.get_model('main_app', 'Shoe')
    unique_brands = apps.get_model('main_app', 'UniqueBrands')
    db_alias = scheme_editor.connection.alias

    unique_brand_names = shoe.objects.values_list('brand', flat=True).distinct()

    for brand_name in unique_brand_names:
        unique_brands.objects.using(db_alias).create(brand_name=brand_name)


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_uniquebrands'),
    ]

    operations = [
        migrations.RunPython(create_unique_brands)
    ]
