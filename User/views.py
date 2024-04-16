from .form import CustomUserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.views import FormView
from django.contrib import messages
from django.contrib.auth.views import LoginView as Login, LogoutView as Logout

User = get_user_model()

from django.contrib import messages
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login

class UserRegistrationView(FormView):
    template_name = 'user/Login.html'
    form_class = CustomUserCreationForm
    model = User
    success_url = '/'

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Account was created successfully!    ')
        return super().form_valid(form)

class LoginView(BaseLoginView):
    template_name = 'user/login.html'
    form_class = AuthenticationForm

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        messages.success(self.request, 'You have been logged in successfully!')
        return super().form_valid(form)

    template_name = "user/Login.html"


class LogoutView(Logout):
    pass
