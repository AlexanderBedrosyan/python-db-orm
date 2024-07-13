from django.core.exceptions import ValidationError
from django.db import models
from datetime import date

# Create your models here.


from django.core.exceptions import ValidationError
from django.db import models
from datetime import date

# Create your models here.



class Employee(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=10)

    class Meta:
        abstract = True


class SpecialtiesChoices(models.TextField):
    MAMMALS = 'Mammals', 'Mammals'
    BIRDS = 'Birds', 'Birds'
    REPTILES = 'Reptiles', 'Reptiles'
    OTHERS = 'Others', 'Others'


class ZooKeeper(Employee):
    class SpecialtiesChoices(models.TextChoices):
        MAMMALS = 'Mammals', 'Mammals'
        BIRDS = 'Birds', 'Birds'
        REPTILES = 'Reptiles', 'Reptiles'
        OTHERS = 'Others', 'Others'


    specialty = models.CharField(max_length=10, choices=SpecialtiesChoices.choices)
    managed_animals = models.ManyToManyField(
        to=Animal
    )

    def clean(self):
        super().clean()

        list_of_choices = [choice[0] for choice in self.SpecialtiesChoices.choices]

        if self.specialty not in list_of_choices:
            raise ValidationError(
                'Specialty must be a valid choice.'
            )


