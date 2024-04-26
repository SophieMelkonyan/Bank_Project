from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, TemplateView
from .models import Profile
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.views import FormView
from django.contrib import messages
from .form import ProfileForm, EmailForm, CustomUserCreationForm
from django.contrib.auth import authenticate, login
from .tasks import send_simple_email
from django.template.loader import render_to_string
from .generate_token import account_activation_token
from django.contrib.sites.shortcuts import get_current_site


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


def prof_form(request):
    form = ProfileForm()

    print(form.fields)
    return render(request, "profile/profile.html", {'form': form})









