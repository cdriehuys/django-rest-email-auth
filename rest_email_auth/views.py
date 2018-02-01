"""Views for the ``rest_email_auth`` app.
"""

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from rest_email_auth import serializers
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
