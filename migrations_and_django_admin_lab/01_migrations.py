from django.db import models


# 1. Terminal steps:
# python manage.py makemigrations
# python manage.py migrate


# 2. Execute all line inside caller.py till row 80 (inclusive)
# Message - 3 products were added successfully to the database

# 3. Add in the model 2 new columns:

class Product(models.Model):
    name = models.CharField(max_length=500)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100, null=True, blank=True)
    supplier = models.CharField(max_length=150, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True, editable=False) # New added
    last_edited_on = models.DateTimeField(auto_now=True, editable=False) # New added

# Migrate it, as use the default timezone.now for the option to not quit the migration.

# 4. Run code on row 82 inside caller.py
# Result - 1 product with time of creation and edition was added to the database

# 5. Add new column Count to the model


class Product(models.Model):
    name = models.CharField(max_length=500)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100, null=True, blank=True)
    supplier = models.CharField(max_length=150, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True, editable=False)
    last_edited_on = models.DateTimeField(auto_now=True, editable=False)
    count = models.PositiveIntegerField(default=0) # New added

# 6. Run line 84 inside caller.py
# Result - 2 products with count were added to the database

# 7. Undo last migration:
# python manage.py migrate main_app 0002
# You can check the result in the table "product" or by using python manage.py showmigration we can see that the
# migration 0003_product_count is empty [ ]

# 8. Change the columns category and supplier as they should NOT be optionals:

class Product(models.Model):
    name = models.CharField(max_length=500)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100) # changes
    supplier = models.CharField(max_length=150) # changes
    created_on = models.DateTimeField(auto_now_add=True, editable=False)
    last_edited_on = models.DateTimeField(auto_now=True, editable=False)

# Migrate the changes
# There is no explanation what kind of default options they need therefore I used None for both.