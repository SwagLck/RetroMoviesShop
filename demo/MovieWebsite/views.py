from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from .models import Movie, TvShow
from .forms import ProfileForm, UserForm
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
