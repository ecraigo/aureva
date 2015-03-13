# This is for creating form classes for all the possible forms on the website. This file will eventually be very long.
from django import forms
from aureva_core.models import User, UserProfile

# Either 'fields' or 'exclude' must explici

class UserForm(forms.ModelForm):  # ModelForm automatically generates a form from a model
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['tagline', 'biography', 'location', 'profile_image']