from .views import options_view,ServiceView,ServiceListView,ServiceDeleteView
from django.urls import path
app_name = "service"

urlpatterns = [
    path("", options_view, name="options"),
    path("service/", ServiceView.as_view(), name="service"),
    path("worker/", ServiceListView.as_view(), name="worker"),
    path('delete/<int:service_id>/', ServiceDeleteView.as_view(), name='delete'),




]
