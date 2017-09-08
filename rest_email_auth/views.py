"""Views for the ``rest_email_auth`` app.
"""

from rest_framework import generics, status

from rest_email_auth import serializers


class EmailVerificationView(generics.CreateAPIView):
    """
    Verify a user's email address.
    """
    serializer_class = serializers.EmailVerificationSerializer

    def create(self, request, *args, **kwargs):
        """
        Override the create method to return a 200 response.

        Args:
            request:
                The request being made.
            args:
                The arguments to pass to the parent create method.
            kwargs:
                The keyword arguments to pass to the parent create
                method.

        Returns:
            A response with a 200 status code.
        """
        response = super(EmailVerificationView, self).create(
            request, *args, **kwargs)
        response.status_code = status.HTTP_200_OK

        return response


class RegistrationView(generics.CreateAPIView):
    """
    Register a new user.
    """
    serializer_class = serializers.RegistrationSerializer
