from .views import RegistrationView, login_view, CreateProfile, ValidateUserLink
from django.urls import path


app_name = "user"

urlpatterns = [
    path("", RegistrationView.as_view(), name="register"),
    path("login/", login_view, name="login"),
    path("<int:pk>/<str:token>/", ValidateUserLink.as_view(), name="verify"),
    path("profile/<int:pk>/",CreateProfile.as_view(), name="profile"),



]