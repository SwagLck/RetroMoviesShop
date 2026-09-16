from django.shortcuts import render
from .models import Movie, TvShow

# Create your views here.
def home(request):
    return render(request, "home.html")

def movies(request):
    items = Movie.objects.all()
    return render(request, "movies.html", {"movies": items})

def tvshows(request):
    items = TvShow.objects.all()
    return render(request, "tvshows.html", {"tvshows": items})