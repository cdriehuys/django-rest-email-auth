"""Views for the ``rest_email_auth`` app.
"""

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from rest_email_auth import app_settings, serializers
from rest_email_auth.generics import SerializerSaveView


class EmailDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    delete:
    Delete a specific email address.

    get:
    Retrieve the details of a particular email address.

    patch:
    Partially update an email address.

    Only a verified email address may be marked as the user's primary
    email.

    put:
    Update an email address.

    Only a verified emaili address may be marked as the user's primary
    email.
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.EmailSerializer

    def get_queryset(self):
        """
        Get the email addresses belonging to the requesting user.

        Returns:
            A queryset containing only the email addresses owned by the
            requesting user.
        """
        return self.request.user.email_addresses.all()


class EmailListView(generics.ListCreateAPIView):
    """
    get:
    List the email addresses associated with the requesting user's
    account.

    post:
    Add a new email address to the requesting user's account.
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.EmailSerializer

    def get_queryset(self):
        """
        Get the email addresses belonging to the requesting user.

        Returns:
            A queryset containing only the email addresses owned by the
            requesting user.
        """
        return self.request.user.email_addresses.all()

    def perform_create(self, serializer):
        """
        Create a new email address attached to the requesting user.

        Args:
            serializer:
                An instance of the view's serializer class containing
                the data submitted in the request.

        Returns:
            The newly created email address.
        """
        return serializer.save(user=self.request.user)


class EmailVerificationView(SerializerSaveView):
    """
    Verify a user's email address.
    """

    serializer_class = serializers.EmailVerificationSerializer


class PasswordResetRequestView(SerializerSaveView):
    """
    post:
    Request a password reset for the user with the provided email
    address. A reset token will be generated and emailed to the user.

    Notes:
    * The provided email address must be verified.
    * The operation will appear successful even if no reset email is
      sent. This is done to avoid leaking email addresses.
    """

    serializer_class = serializers.PasswordResetRequestSerializer


class PasswordResetView(SerializerSaveView):
    """
    post:
    Reset the user's password using the token that was emailed to them.
    """

    serializer_class = serializers.PasswordResetSerializer


class RegistrationView(generics.CreateAPIView):
    """
    Register a new user.
    """

    def get_serializer_class(self):
        """
        Get the serializer class used to register new users.
        """
        return app_settings.REGISTRATION_SERIALIZER


class ResendVerificationView(SerializerSaveView):
    """
    Resend an email verification to a specific address.
    """

    serializer_class = serializers.ResendVerificationSerializer
