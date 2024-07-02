# In models.py
from django.db import models
from datetime import date

# Create your models here.


class Artifact(models.Model):
    name = models.CharField(max_length=70)
    origin = models.CharField(max_length=70)
    age = models.PositiveIntegerField()
    description = models.TextField()
    is_magical = models.BooleanField(default=False)

# In caller.py

import os
import django
from datetime import date, datetime

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Pet, Artifact


def create_artifact(name: str, origin: str, age: int, description: str, is_magical: bool) -> str:
    Artifact.objects.bulk_create(
        [
            Artifact(
                name=name,
                origin=origin,
                age=age,
                description=description,
                is_magical=is_magical
            )
        ]
    )

    return f"The artifact {name} is {age} years old!"


def rename_artifact(artifact: Artifact, new_name: str) -> None:
    if artifact.is_magical and artifact.age > 250:
        artifact.name = new_name
        artifact.save()


def delete_all_artifacts() -> None:
    Artifact.objects.all().delete()
