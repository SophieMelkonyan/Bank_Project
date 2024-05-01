
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.contrib.auth import views as auth_views

urlpatterns = i18n_patterns(
path("admin/", include("admin_honeypot.urls", namespace="admin_honeypot")),
path("secret/", admin.site.urls),
    path("", include("User.url", namespace="User")),
    path("change-password/", auth_views.PasswordChangeView.as_view()),
    path("reset-password/", auth_views.PasswordResetView.as_view(), name="reset_password"),
    path("password-reset-done/", auth_views.PasswordResetDoneView.as_view(),
         name="password_reset_done"),
    path("password-reset-confirm/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(),
         name="password_reset_confirm"),
    path("password-reset-complete/", auth_views.PasswordResetCompleteView.as_view(),
         name="password_reset_complete"),
    path("home/", include("home.url", namespace="home")),
    path("services/", include("check.url", namespace="service")),
)
