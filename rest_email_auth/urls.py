"""
URL configuration for the ``rest_email_auth`` app.
"""

from django.urls import path

from rest_email_auth import views


app_name = "rest-email-auth"


urlpatterns = [
    path(r"emails/", views.EmailListView.as_view(), name="email-list"),
    path(
        r"emails/<int:pk>/",
        views.EmailDetailView.as_view(),
        name="email-detail",
    ),
    path(r"register/", views.RegistrationView.as_view(), name="register"),
    path(
        r"request-password-reset/",
        views.PasswordResetRequestView.as_view(),
        name="password-reset-request",
    ),
    path(
        r"resend-verification/",
        views.ResendVerificationView.as_view(),
        name="resend-verification",
    ),
    path(
        r"reset-password/",
        views.PasswordResetView.as_view(),
        name="password-reset",
    ),
    path(
        r"verify-email/",
        views.EmailVerificationView.as_view(),
        name="verify-email",
    ),
]
