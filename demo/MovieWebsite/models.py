from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Movie(models.Model):
    title = models.CharField(max_length=200)
    year = models.IntegerField()

class TvShow(models.Model):
    title = models.CharField(max_length=200)
    year = models.IntegerField()
    toyear = models.IntegerField()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    biography=models.CharField(max_length=300)
    favorite_genre=models.CharField(max_length=50)
