from django.core import validators
from django.core.exceptions import ValidationError
from django.db import models
from datetime import date, datetime, timedelta

# Create your models here.

from django.db import models



class MaskedCreditCardField(models.CharField):

    def __init__(self, *args,  **kwargs):
        kwargs['max_length'] = 20
        super().__init__(*args, **kwargs)

    def to_python(self, value):
        if type(value) is not str:
            raise ValidationError("The card number must be a string")

        if not value.isdigit():
            raise ValidationError("The card number must contain only digits")

        if len(value) != 16:
            raise ValidationError("The card number must be exactly 16 characters long")

        last_four_card_digits = value[-4:]
        return f"****-****-****-{last_four_card_digits}"


class CreditCard(models.Model):
    card_owner = models.CharField(max_length=100)
    card_number = MaskedCreditCardField()
