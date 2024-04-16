from .views import UserRegistrationView
from django.urls import path


app_name = "user"

urlpatterns = [
    path("", UserRegistrationView.as_view(), name="login"),

]