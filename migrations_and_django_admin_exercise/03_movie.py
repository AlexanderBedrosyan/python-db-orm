from django.db import models
from datetime import date

# Create your models here.


class Movie(models.Model):
    title = models.CharField(max_length=100)
    director = models.CharField(max_length=100)
    release_year = models.PositiveIntegerField()
    genre = models.CharField(max_length=50)

    def __str__(self):
        return f'Movie "{self.title}" by {self.director}'


from django.contrib import admin
from main_app.models import Movie # it must be without main_app, it's added only for this py file

# Register your models here.



@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'director', 'release_year', 'genre')
    list_filter = ('release_year', 'genre')
    search_fields = ('title', 'director')