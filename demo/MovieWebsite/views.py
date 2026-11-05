from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from .models import Movie, TvShow
from .forms import ProfileForm, UserForm
from django.contrib.auth.decorators import login_required, user_passes_test

# Create your views here.
def home(request):
    return render(request, "home.html")

def movies(request):
    items = Movie.objects.prefetch_related("genres").order_by("-year", "title")
    page = Paginator(items, 24).get_page(request.GET.get("page"))
    return render(request, "movies.html", {"movies": page, "page_obj": page})


def tvshows(request):
    items = TvShow.objects.prefetch_related("genres").order_by("-year", "title")
    page = Paginator(items, 24).get_page(request.GET.get("page"))
    return render(request, "tvshows.html", {"tvshows": page, "page_obj": page})


def movie_detail(request, pk):
    movie = get_object_or_404(Movie.objects.prefetch_related("genres"), pk=pk)
    return render(request, "movie_detail.html", {"movie": movie})

def tvshow_detail(request, pk):
    tvshow = get_object_or_404(TvShow.objects.prefetch_related("genres"), pk=pk)
    return render(request, "tvshow_detail.html", {"tvshow": tvshow})

@login_required
@user_passes_test(lambda u: u.is_staff)
def userslist(request):
    users = User.objects.all()
    return render(request, "userslist.html", {"users": users})

@login_required
def profile(request, username):
    profile_user = get_object_or_404(User, username = username)

    user_profile = profile_user.profile

    return render(request, "profile.html", {
        "profile_user": profile_user,
        "profile": user_profile,
    })

@login_required
def edit_profile(request):
    profile = request.user.profile

    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect("profile", username=request.user.username)
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)
    return render(request, "edit_profile.html", {
        "user_form": user_form,
        "profile_form": profile_form,
    })
