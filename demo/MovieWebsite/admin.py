from django.contrib import admin
from .models import Movie, TvShow, Profile

# Register your models here.

admin.site.register(Movie)
admin.site.register(TvShow)
admin.site.register(Profile)