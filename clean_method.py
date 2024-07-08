from django.core.exceptions import ValidationError
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def clean(self):
        # Персонализирана валидация: Уверете се, че цената на отстъпката не е по-висока от оригиналната цена
        if self.discount_price and self.discount_price > self.price:
            raise ValidationError('Discount price cannot be greater than the original price.')

    def save(self, *args, **kwargs):
        # Извикване на clean() преди запазването на обекта
        self.clean()
        super().save(*args, **kwargs)


# Методът clean()
# Методът clean() се използва за персонализирана валидация на данни в моделите. Той се извиква преди запазването на обект,
# за да се гарантира, че данните са валидни.