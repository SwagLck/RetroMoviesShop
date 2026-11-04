from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Genre(models.Model):
    tmdb_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Movie(models.Model):
    tmdb_id = models.IntegerField(unique=True, null=True, blank=True)
    title = models.CharField(max_length=200)
    year = models.IntegerField(null=True, blank=True)
    overview = models.TextField(blank=True)
    poster_path = models.CharField(max_length=200, blank=True)
    genres = models.ManyToManyField(Genre, blank=True)

class TvShow(models.Model):
    tmdb_id = models.IntegerField(unique=True, null=True, blank=True)
    title = models.CharField(max_length=200)
    year = models.IntegerField(null=True, blank=True)
    toyear = models.IntegerField(null=True, blank=True)
    overview = models.TextField(blank=True)
    poster_path = models.CharField(max_length=200, blank=True)
    genres = models.ManyToManyField(Genre, blank=True)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    biography=models.CharField(max_length=300)
    favorite_genre=models.CharField(max_length=50)
