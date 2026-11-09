from django import forms
from .models import Profile, Comment
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["biography", "favorite_genre"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["rating", "text"]
        widgets = {
            "rating": forms.HiddenInput(),
            "text": forms.Textarea(attrs={
                "rows": 3,
                "class": "form-control",
                "placeholder": "Write a comment..."
            }),
        }


