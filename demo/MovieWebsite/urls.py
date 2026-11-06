from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("Movies/", views.movies, name="movies"),
    path("movie/<int:pk>/", views.movie_detail, name="movie_detail"),
    path("TvShows/", views.tvshows, name="tvshows"),
    path("TvShows/<int:pk>/", views.tvshow_detail, name="tvshow_detail"),
    path("comments/<int:pk>/delete/", views.delete_comment, name="delete_comment"),
    path("Users/", views.userslist, name="userslist"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path("profile/<str:username>/", views.profile, name="profile"),
    path("profile/<str:username>/toggle-block/", views.toggle_block_user, name="toggle_block_user"),
]