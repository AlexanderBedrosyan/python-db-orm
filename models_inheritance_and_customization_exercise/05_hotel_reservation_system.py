from django.core import validators
from django.core.exceptions import ValidationError
from django.db import models
from datetime import date, datetime, timedelta

# Create your models here.

from django.db import models


class Hotel(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)


class Room(models.Model):
    hotel = models.ForeignKey(
        to=Hotel,
        on_delete=models.CASCADE
    )
    number = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField()
    total_guests = models.PositiveIntegerField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)

    def clean(self):
        if self.total_guests > self.capacity:
            raise ValidationError("Total guests are more than the capacity of the room")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
        return f"Room {self.number} created successfully"


class BaseReservation(models.Model):

    room = models.ForeignKey(
        to=Room,
        on_delete=models.CASCADE
    )
    start_date = models.DateField()
    end_date = models.DateField()

    def reservation_period(self):
        date_difference = self.end_date - self.start_date

        return date_difference.days

    def calculate_total_cost(self):
        return round(self.room.price_per_night * self.reservation_period(), 2)

    @property
    def is_available(self) -> bool:

        reservations = self.__class__.objects.filter(
            room=self.room,
            end_date__gte=self.start_date,
            start_date__lte=self.end_date,
        )

        return not reservations.exists()

    def clean(self) -> None:
        if self.start_date >= self.end_date:
            raise ValidationError("Start date cannot be after or in the same end date")

        if not self.is_available:
            raise ValidationError(f"Room {self.room.number} cannot be reserved")

    class Meta:
        abstract = True


class RegularReservation(BaseReservation):

    def save(self, *args, **kwargs) -> str:
        super().clean()

        super().save(*args, **kwargs)

        return f"Regular reservation for room {self.room.number}"


class SpecialReservation(BaseReservation):

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

        return f"Special reservation for room {self.room.number}"

    def extend_reservation(self, days: int) -> str:
        self.end_date += timedelta(days=days)

        if not self.is_available:
            raise ValidationError("Error during extending reservation")

        self.save()

        return f"Extended reservation for room {self.room.number} with {days} days"
