from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("Movies/", views.movies, name="movies"),
    path("movie/<int:pk>/", views.movie_detail, name="movie_detail"),
    path("TvShows/", views.tvshows, name="tvshows"),
    path("TvShows/<int:pk>/", views.tvshow_detail, name="tvshow_detail"),
    path("comments/<int:pk>/delete/", views.delete_comment, name="delete_comment"),
    path("comments/<int:pk>/hide/", views.toggle_hide_comment, name="toggle_hide_comment"),
    path("comments/<int:pk>/report/", views.report_comment, name="report_comment"),
    path("reports/", views.reports_list, name="reports_list"),
    path("Users/", views.userslist, name="userslist"),
    path("Order/", views.order, name="order"),
    path("Subscriptions/", views.subscriptions, name="subscriptions"),
    path("AdminPanel/", views.admin_panel, name="admin_panel"),
    path("DiscountAdd/", views.discount_add, name="discount_add"),
    path("OrderHistory/", views.history, name="history"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path("profile/<str:username>/", views.profile, name="profile"),
    path("profile/<str:username>/toggle-block/", views.toggle_block_user, name="toggle_block_user"),
    path("", views.home, name="home"),
    path("MovieStatistics/", views.movie_statistics, name="movie_statistics"),
    path(
    "comments/<int:pk>/edit/",views.edit_comment,name="edit_comment")
]