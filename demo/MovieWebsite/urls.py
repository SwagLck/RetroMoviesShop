from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("Movies/", views.movies, name="movies"),
    path("TvShows/", views.tvshows, name="tvshows"),
]