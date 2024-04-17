from .views import Home
from django.urls import path


app_name = "home"

urlpatterns = [
    path("", Home.as_view(), name="home"),


]