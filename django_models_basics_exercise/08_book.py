from django.db import models

# Create your models here.


class Book(models.Model):
    class GenreChoices(models.TextChoices):
        FICTION = 'Fi', 'Fiction'
        NON_FICTION = 'No-Fi', 'Non-Fiction'
        SCIENCE_FICTION = 'SF', 'Science Fiction'
        HORROR = 'HR', 'Horror'
    title = models.CharField(max_length=30)
    author = models.CharField(max_length=100)
    genre = models.CharField(max_length=20, choices=GenreChoices.choices)
    publication_date = models.DateField(editable=False, auto_now_add=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_available = models.BooleanField(default=True)
    rating = models.FloatField()
    description = models.TextField()

    def __str__(self):
        return self.title