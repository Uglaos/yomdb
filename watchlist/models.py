from django.db import models


class Watchlist(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Movie(models.Model):
    imdbID = models.CharField(max_length=50)
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title
