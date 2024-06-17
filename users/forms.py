from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
    UserChangeForm,
)

from users.models import User


class UserLoginForm(AuthenticationForm):

    username = forms.CharField()
    password = forms.CharField()

    # username = forms.CharField(
    #     label= "Username",
    #     widget=forms.TextInput(attrs={"autofocus": True,
    #                                   "class": "form-control",
    #                                   "placeholder": "Enter your username"})
    # )
    # password = forms.CharField(
    #     label= "Password",
    #     widget=forms.TextInput(attrs={"autocomplete": "current-password",
    #                                   "class": "form-control",
    #                                   "placeholder": "Enter password"})
    # )
    class Meta:
        model = User
        fields = ["username", "password"]


class UserRegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
        )

    first_name = forms.CharField(label="First name*")
    last_name = forms.CharField(label="Last name*")
    username = forms.CharField(label="Username*")
    email = forms.CharField(label="Email*")
    password1 = forms.CharField(label="Password*")
    password2 = forms.CharField(label="Confirm the password*")


class ProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = (
            "image",
            "first_name",
            "last_name",
            "username",
            "email",
        )

    image = forms.ImageField(required=False)
    first_name = forms.CharField(label="First name*")
    last_name = forms.CharField(label="Last name*")
    username = forms.CharField(label="Username*")
    email = forms.CharField(label="Email*")
