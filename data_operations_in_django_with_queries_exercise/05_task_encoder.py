# In models.py
from django.db import models
from datetime import date

# Create your models here.


class Task(models.Model):
    title = models.CharField(max_length=25)
    description = models.TextField()
    due_date = models.DateField()
    is_finished = models.BooleanField(default=False)
   

# In caller.py
import os
import django
from datetime import date, datetime

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Pet, Artifact, Location, Car, Task


def show_unfinished_tasks():
    return '\n'.join([f'Task - {task.title} needs to be done until {task.due_date}!' for task in Task.objects.all()])


def complete_odd_tasks():
    all_tasks = Task.objects.all()
    update_tasks = []

    for task in all_tasks:
        if task.pk % 2 != 0:
            task.is_finished = True
            update_tasks.append(task)

    Task.objects.bulk_update(update_tasks, ['is_finished'])


def encode_and_replace(text:str, task_title: str) -> None:
    all_tasks = Task.objects.filter(title=task_title)
    updated_descriptions = []

    encoded_message = ''.join([chr(ord(ch) - 3) for ch in text])

    for task in all_tasks:
        task.description = encoded_message
        updated_descriptions.append(task)

    Task.objects.bulk_update(updated_descriptions, ['description'])
