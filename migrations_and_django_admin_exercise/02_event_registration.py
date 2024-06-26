from django.db import models
from datetime import date

# Create your models here.


class EventRegistration(models.Model):
    event_name = models.CharField(max_length=60)
    participant_name = models.CharField(max_length=50)
    registration_date = models.DateField()

    def __str__(self):
        return f"{self.participant_name} - {self.event_name}"

from django.contrib import admin
from main_app.models import EventRegistration # it must be without main_app, it's added only for this py file

# Register your models here.


@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ('event_name', 'participant_name', 'registration_date')
    list_filter = ('event_name', 'registration_date')
    search_fields = ('event_name', 'participant_name')

