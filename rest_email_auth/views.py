"""Views for the ``rest_email_auth`` app.
"""

from rest_framework import generics

from rest_email_auth import serializers
from rest_email_auth.generics import SerializerSaveView


class EmailVerificationView(SerializerSaveView):
    """
    Verify a user's email address.
    """
    serializer_class = serializers.EmailVerificationSerializer


class RegistrationView(generics.CreateAPIView):
    """
    Register a new user.
    """
    serializer_class = serializers.RegistrationSerializer


class ResendVerificationView(SerializerSaveView):
    """
    Resend an email verification to a specific address.
    """
    serializer_class = serializers.ResendVerificationSerializer
