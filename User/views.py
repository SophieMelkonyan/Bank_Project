from django.shortcuts import render, redirect

from .form import CustomUserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.views import FormView
from django.contrib import messages

from django.contrib.auth import authenticate, login


User = get_user_model()


class UserRegistrationView(FormView):
    template_name = 'user/Login.html'
    form_class = CustomUserCreationForm
    model = User
    success_url = '/'



    def form_valid(self, form):
        form.save()
        messages.success(self.request,"You have successfully registered")
        return super().form_valid(form)


def login_view(request):

    if(request.method == 'POST'):
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect("home:home")
        else:

            return render(request, 'user/login.html', {'email': email})




