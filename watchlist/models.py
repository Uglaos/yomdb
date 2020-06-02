from django.db import models
from django.shortcuts import reverse


class Actor(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Movie(models.Model):
    imdbID = models.CharField(max_length=50)
    title = models.CharField(max_length=200)
    watched = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)
    actors = models.ManyToManyField(Actor)
    genres = models.ManyToManyField(Genre)
    slug = models.SlugField()

    def __str__(self):
        return self.title
