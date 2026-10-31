from django.shortcuts import render, redirect
from MovieWebsite.models import Profile
from .forms import RegisterForm

# Create your views here.
def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            new_user = form.save()
            Profile.objects.create(user=new_user)
            return redirect("home")
    else:
        form = RegisterForm()
    return render(response, "register/register.html", {"form": form})