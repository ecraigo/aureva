# This is for creating form classes for all the possible forms on the website. This file will eventually be very long.
from django import forms
from aureva_core.models import User, UserProfile


class UserForm(forms.ModelForm):  # ModelForm automatically generates a form from a model
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']  # Ether 'fields' or 'exclude' must
                                                                               # explicitly be passed


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['style', 'biography']