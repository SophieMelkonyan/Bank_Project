from .views import UserRegistrationView, login_view,ProfileView1,ProfileUpdateView
from django.urls import path


app_name = "user"

urlpatterns = [
    path("", UserRegistrationView.as_view(), name="register"),
    path("login/", login_view, name="login"),
    path("profile/<int:pk>/", ProfileView1.as_view(), name="profile"),
    path('profile/update/', ProfileUpdateView.as_view(), name='profile_update'),


 

]