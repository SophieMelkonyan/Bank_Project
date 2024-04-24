from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView
from .models import Profile
from .form import CustomUserCreationForm,ProfileForm
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
            print(request.user.id)
            return redirect("user:profile", pk=request.user.id)
        else:

            return render(request, 'user/login.html', {'email': email})

    return HttpResponse(render(request, "user/login.html"))


class CreateProfile(DetailView):
    model = Profile

    template_name = 'profile/profile.html'

    context_object_name = "profile"

    def get_object(self, queryset=None):
        pk = self.request.user.pk
        User = get_user_model()
        user = get_object_or_404(User, pk=pk)
        profile = user.profile
        return profile


class ProfileView(FormView):
    template_name = 'profile/profile.html'
    form_class = ProfileForm
    model = Profile
    success_url = '/'

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "You have successfully registered")
        return super().form_valid(form)


class ProfileView1(DetailView, FormView):
    model = Profile
    template_name = 'profile/profile.html'
    context_object_name = 'profile'
    form_class = ProfileForm
    success_url = '/'

    def get_object(self, queryset=None):
        pk = self.request.user.pk
        User = get_user_model()
        user = get_object_or_404(User, pk=pk)
        profile = user.profile
        return profile

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "You have successfully registered")
        return super().form_valid(form)


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = 'profile/profile.html'
    form_class = ProfileForm
    success_url = reverse_lazy('user:profile_update')

    def get_object(self, queryset=None):
        return self.request.user.profile

    def form_valid(self, form):
        messages.success(self.request, "Profile updated successfully")
        return super().form_valid(form)






