"""
URL configuration for the ``rest_email_auth`` app.
"""

from django.conf.urls import url

from rest_email_auth import views


app_name = 'rest-email-auth'


urlpatterns = [
    url(
        r'^register/$',
        views.RegistrationView.as_view(),
        name='register'),

    url(
        r'^resend-verification/$',
        views.ResendVerificationView.as_view(),
        name='resend-verification'),

    url(
        r'^verify-email/$',
        views.EmailVerificationView.as_view(),
        name='verify-email'),
]
