from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=100)
    release_date = models.DateField()
    genre = models.CharField(max_length=50)
    duration_minutes = models.IntegerField()
    rating = models.FloatField()

    def __str__(self):
        return self.title

# Create your models here.
