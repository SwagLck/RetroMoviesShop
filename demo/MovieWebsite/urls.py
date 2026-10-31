from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("Movies/", views.movies, name="movies"),
    path("TvShows/", views.tvshows, name="tvshows"),
    path("Users/", views.userslist, name="userslist"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path("profile/<str:username>/", views.profile, name="profile")
]