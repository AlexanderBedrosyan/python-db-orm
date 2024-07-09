from django.db import models

class BooleanChoiceField(models.BooleanField):
    def __init__(self, *args, **kwargs):
        kwargs['choices'] = (
            (True, 'Available'),
            (False, 'Not Available'),
        )
        kwargs['default'] = True
        super().__init__(*args, **kwargs)

    def from_db_value(self, value, expression, connection):
        # Преобразува стойността от базата данни към Python обект.
        # Ако стойността е None, връща None.
        # В противен случай връща True или False в зависимост от стойността в базата данни.
        if value is None:
            return value
        return bool(value)

    def to_python(self, value):
        # Преобразува стойността към Python обект (използва се и при десериализация и форми)
        if value in (True, False):
            return value
        if value is None:
            return value
        return bool(value)

    def get_prep_value(self, value):
        # Преобразува стойността към формат, подходящ за съхранение в базата данни.
        if value is None:
            return None
        return bool(value)

# Примерен модел, използващ персонализираното поле BooleanChoiceField
class Veterinarian(models.Model):
    license_number = models.CharField(max_length=10)
    availability = BooleanChoiceField()

# Създаване на нов ветеринар
vet1 = Veterinarian.objects.create(license_number='12345', availability=True)
vet2 = Veterinarian.objects.create(license_number='54321', availability='1')  # Стойността "1" ще бъде конвертирана към
# True
vet3 = Veterinarian.objects.create(license_number='98765', availability='False')  # Стойността "False" ще бъде
# конвертирана към True (тъй като непразни стрингове се конвертират към True)
