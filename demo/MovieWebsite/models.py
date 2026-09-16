from django.db import models

# Create your models here.

class Movie(models.Model):
    title = models.CharField(max_length=200)
    year = models.IntegerField()

class TvShow(models.Model):
    title = models.CharField(max_length=200)
    year = models.IntegerField()
    toyear = models.IntegerField()