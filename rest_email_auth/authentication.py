"""
Authentication backends to handle authenticating with any of a user's
email addresses.
"""

from django.contrib.auth import get_user_model

from rest_email_auth import models


class BaseBackend(object):
    """
    Base class for authentication backends.
    """

    def get_user(self, user_id):
        """
        Get a user by their ID.

        Args:
            user_id:
                The ID of the user to fetch.

        Returns:
            The user with the specified ID if they exist and ``None``
            otherwise.
        """
        try:
            return get_user_model().objects.get(id=user_id)
        except get_user_model().DoesNotExist:
            return None


class VerifiedEmailBackend(BaseBackend):
    """
    Authentication backend that only allows for the use of verified
    email addresses.
    """

    def authenticate(self, request, email=None, password=None, username=None):
        """
        Attempt to authenticate a set of credentials.

        Args:
            request:
                The request associated with the authentication attempt.
            email:
                The user's email address.
            password:
                The user's password.
            username:
                An alias for the ``email`` field. This is provided for
                compatability with Django's built in authentication
                views.

        Returns:
            The user associated with the provided credentials if they
            are valid. Returns ``None`` otherwise.
        """
        email = email or username

        try:
            email_instance = models.EmailAddress.objects.get(
                is_verified=True, email=email
            )
        except models.EmailAddress.DoesNotExist:
            return None

        user = email_instance.user

        if user.check_password(password):
            return user

        return None
