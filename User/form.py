
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
        fields = ['balance']
        labels = {'balance': 'Balance'}


class Bankomat(forms.ModelForm):

    money = forms.DecimalField(max_digits=10, decimal_places=2)
    pin_code = forms.IntegerField(widget=forms.PasswordInput(attrs={"id": "pinpad-input"}))


    class Meta:
        model = Profile
        fields = ['money','pin_code']






