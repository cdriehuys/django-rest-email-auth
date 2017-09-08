"""Views for the ``rest_email_auth`` app.
"""

from rest_framework import generics

from rest_email_auth import serializers


class RegistrationView(generics.CreateAPIView):
    """
    Register a new user.
    """
    serializer_class = serializers.RegistrationSerializer
