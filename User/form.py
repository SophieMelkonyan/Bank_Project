from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Profile


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email','password1', 'password2', 'first_name', 'last_name',]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['pin_code', 'balance']
        labels = {'pin_code': 'Pin Code', 'balance': 'Balance'}



