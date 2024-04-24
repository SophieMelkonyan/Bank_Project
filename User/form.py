
from .models import Profile
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class EmailForm(forms.Form):
    email = forms.EmailField()
    subject = forms.CharField()
    body = forms.CharField(widget=forms.Textarea())


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'password1', 'password2', 'first_name', 'last_name',]

        def save(self, commit=True):
            user = super().save(commit=False)

            if commit:
                user.save()
            return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['pin_code', 'balance']
        labels = {'pin_code': 'Pin Code', 'balance': 'Balance'}



