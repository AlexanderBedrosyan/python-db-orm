from django.db import models

# Create your models here.


class Exercise(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    difficulty_level = models.CharField(max_length=20)
    duration_minutes = models.PositiveIntegerField()
    equipment = models.CharField(max_length=90)
    video_url = models.URLField(blank=True, null=True)
    calories_burned = models.PositiveIntegerField(default=1)
    is_favorite = models.BooleanField(default=False)