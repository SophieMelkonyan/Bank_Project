from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, TemplateView
from .models import Profile
from django.contrib.auth.models import Group
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.views import FormView
from django.contrib import messages
from .form import ProfileForm, EmailForm, CustomUserCreationForm,Bankomat
from django.contrib.auth import authenticate, login
from .tasks import send_simple_email
from django.template.loader import render_to_string
from .generate_token import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from helpers.decoraters import OwnProFileMixin


User = get_user_model()



class EmailView(FormView):
    template_name = "users/send_simple_email.html"
    form_class = EmailForm
    success_url = "/"

    def form_valid(self, form):
        response = super().form_valid(form)
        email = form.cleaned_data["email"]
        subject = form.cleaned_data["subject"]
        body = form.cleaned_data["body"]

        send_simple_email.apply_async(kwargs={"body": body, "subject": subject,
                                              "email": email, "count": 10})
        return response


class RegistrationView(CreateView):
    form_class = CustomUserCreationForm
    model = User
    template_name = "user/Login.html"
    success_url = "/"

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        customer_group = Group.objects.get(name='customer')
        user.groups.add(customer_group)
        subject = "Authenticate your Profile"
        user.is_active = False
        user.save()
        token = account_activation_token.make_token(user)
        message = render_to_string("users/authentication.html",
                                   {"user": user,
                                    "domain": get_current_site(self.request),
                                    "token": token})
        email = EmailMessage(subject=subject, body=message,
                             from_email=settings.EMAIL_HOST_USER,
                             to=[user.email])
        email.send(fail_silently=False)
        messages.success(self.request, "You have successfully registered")
        return response


class ValidateUserLink(TemplateView):

    def get(self, request, *args, **kwargs):
        token = kwargs.get("token")
        pk = kwargs.get("pk")
        user = User.objects.get(pk=pk)
        if account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect("user:login")
        return HttpResponse("Your token is invalid")


def login_view(request):
    if(request.method == 'POST'):
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            if user.groups.filter(name='worker').exists():
                return redirect("service:worker")

            return redirect("user:profile", pk=request.user.id)
        else:

            return render(request, 'user/login.html', {'email': email})

    return HttpResponse(render(request, "user/login.html"))

class UserList(TemplateView):
    template_name = "profile/worker1.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profiles = Profile.objects.all()
        context['profiles'] = profiles
        return context


class CreateProfile(FormView, DetailView):
    model = Profile
    template_name = 'profile/profile.html'
    context_object_name = "profile"
    form_class = ProfileForm
    success_url = None

    def get_object(self, queryset=None):
        pk = self.request.user.pk
        User = get_user_model()
        user = get_object_or_404(User, pk=pk)
        profile = user.profile
        return profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        context['balance'] = profile.balance
        return context

    def form_valid(self, form):
        profile = self.get_object()
        profile.balance += form.cleaned_data["balance"]

        profile.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('user:profile', kwargs={'pk': self.request.user.pk})

class BankomatView(FormView):
    template_name = 'bankomat/bankomat.html'
    form_class = Bankomat
    success_url = None

    def form_valid(self, form):
        money = form.cleaned_data['money']
        pin_code = form.cleaned_data['pin_code']
        profile = Profile.objects.get(user=self.request.user)
        if(pin_code == profile.pin_code):
            if(profile.balance < money ):
                messages.error(self.request, "Your balance is minus")
            profile.balance -= money
            profile.save()
            return redirect(reverse_lazy('user:profile', kwargs={'pk': profile.pk}))
        else:
            messages.error(self.request, "Your pin code is incorrect")

            return redirect('user:bankomate')

