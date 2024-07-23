from decimal import Decimal
from django.core import validators
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator, MinValueValidator, MaxValueValidator, \
    RegexValidator
from django.db import models
from datetime import date, datetime, timedelta
import re
from main_app.validators import VideoGameValidator, release_year_checker

# Create your models here.

from django.db import models
from django.db.models import QuerySet, Q, Count, Avg


class BillingInfo(models.Model):
    address = models.CharField(max_length=200)


class Invoice(models.Model):
    invoice_number = models.CharField(max_length=20, unique=True)
    billing_info = models.OneToOneField(BillingInfo, on_delete=models.CASCADE)

    @classmethod
    def get_invoices_with_prefix(cls, prefix: str):
        return cls.objects.filter(invoice_number__startswith=prefix)

    @classmethod
    def get_invoices_sorted_by_number(cls):
        return cls.objects.all().order_by('invoice_number')

    @classmethod
    def get_invoice_with_billing_info(cls, invoice_number: str):
        return cls.objects.get(invoice_number=invoice_number)
