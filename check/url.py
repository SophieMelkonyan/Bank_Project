from .views import options_view,ServiceView
from django.urls import path
app_name = "service"

urlpatterns = [
    path("", options_view, name="options"),
    path("service/", ServiceView.as_view(), name="service"),




]