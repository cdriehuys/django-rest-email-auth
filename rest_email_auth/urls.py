"""
URL configuration for the ``rest_email_auth`` app.
"""

from django.conf.urls import url

from rest_email_auth import views


urlpatterns = [
    url(r'^register/$', views.RegistrationView.as_view(), name='register'),
    url(r'^verify-email/$', views.EmailVerificationView.as_view(), name='verify-email'),    # noqa
]
