from django.contrib.auth.models import User
from django.shortcuts import render
from .models import Movie, TvShow
from django.contrib.auth.decorators import login_required, user_passes_test

# Create your views here.
def home(request):
    return render(request, "home.html")

def movies(request):
    items = Movie.objects.all()
    return render(request, "movies.html", {"movies": items})

def tvshows(request):
    items = TvShow.objects.all()
    return render(request, "tvshows.html", {"tvshows": items})

@login_required
@user_passes_test(lambda u: u.is_staff)
def userslist(request):
    users = User.objects.all()
    return render(request, "userslist.html", {"users": users})