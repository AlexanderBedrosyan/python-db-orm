from django.db import models
from datetime import date

# Create your models here.


class Blog(models.Model):
    post = models.TextField()
    author = models.CharField(max_length=35)