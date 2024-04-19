from .views import UserRegistrationView, login_view, CreateProfile,prof_form
from django.urls import path


app_name = "user"

urlpatterns = [
    path("", UserRegistrationView.as_view(), name="register"),
    path("login/", login_view, name="login"),
    path("profile/<int:pk>/",CreateProfile.as_view(), name="profile"),


]