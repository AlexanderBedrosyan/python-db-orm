from django.db import models
from datetime import datetime


class Event(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Персонализирана логика преди запазването
        if self.end_date < self.start_date:
            raise ValueError("End date cannot be before start date.")

        # Автоматично задаване на текущата дата и час на updated_at полето
        self.updated_at = datetime.now()

        # Запазване на обекта в базата данни
        super().save(*args, **kwargs)