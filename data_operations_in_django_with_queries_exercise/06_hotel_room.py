# In models.py

from django.db import models
from datetime import date

# Create your models here.


class HotelRoomChoices(models.TextChoices):
    STANDARD = 'ST', 'Standard'
    DELUXE = 'DE', 'Deluxe'
    SUITE = 'SU', 'Suite'


class HotelRoom(models.Model):
    room_number = models.PositiveIntegerField()
    room_type = models.CharField(max_length=10, choices=HotelRoomChoices.choices)
    capacity = models.PositiveIntegerField()
    amenities = models.TextField()
    price_per_night = models.DecimalField(max_digits=8, decimal_places=2)
    is_reserved = models.BooleanField(default=False)


# In caller.py
import os
import django
from datetime import date, datetime

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Pet, Artifact, Location, Car, Task, HotelRoom



def get_deluxe_rooms():
    all_rooms = HotelRoom.objects.all()
    deluxe_rooms = []

    for room in all_rooms:
        if room.room_type == 'Deluxe' and room.pk % 2 == 0:
            deluxe_rooms.append(f'Deluxe room with number {room.room_number} costs {room.price_per_night}$ per night!')

    return '\n'.join(deluxe_rooms)


def increase_room_capacity():
    all_rooms = HotelRoom.objects.all()
    updated_rooms = []

    for i in range(len(all_rooms)):
        current_room = all_rooms[i]

        if current_room.is_reserved:
            if i == 0:
                current_room.capacity += current_room.pk
            else:
                current_room.capacity += all_rooms[i - 1].capacity

            updated_rooms.append(current_room)

    HotelRoom.objects.bulk_update(updated_rooms, ['capacity'])


def reserve_first_room():
    first_room = HotelRoom.objects.first()
    first_room.is_reserved = True
    first_room.save()


def delete_last_room():
    last_room = HotelRoom.objects.last()

    if last_room.is_reserved is False:
        last_room.delete()