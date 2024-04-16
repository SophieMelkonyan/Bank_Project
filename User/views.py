from .form import CustomUserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.views import FormView
from django.contrib import messages
from django.contrib.auth.views import LoginView as Login, LogoutView as Logout

User = get_user_model()

class UserRegistrationView(FormView):
    template_name = 'user/Login.html'
    form_class = CustomUserCreationForm
    model = User
    success_url = '/'


    def form_valid(self, form):

        form.save()
        messages.success(self.request, 'Account was created successfully!')

        return super().form_valid(form)

class LoginView(Login):
    template_name = "user/Login.html"


class LogoutView(Logout):
    pass
