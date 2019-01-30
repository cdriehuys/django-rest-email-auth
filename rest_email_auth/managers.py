from django.db import models, transaction
from django.utils import timezone

from rest_email_auth import app_settings


class EmailAddressManager(models.Manager):
    """
    Manager for email address instances.
    """

    def create(self, *args, **kwargs):
        """
        Create a new email address.
        """
        is_primary = kwargs.pop("is_primary", False)

        with transaction.atomic():
            email = super(EmailAddressManager, self).create(*args, **kwargs)

            if is_primary:
                email.set_primary()

        return email


class ValidPasswordResetTokenManager(models.Manager):
    """
    Manager for getting only valid password reset tokens.

    Valid tokens are those that have not yet expired.
    """

    def get_queryset(self):
        """
        Return all unexpired password reset tokens.
        """
        oldest = timezone.now() - app_settings.PASSWORD_RESET_EXPIRATION
        queryset = super(ValidPasswordResetTokenManager, self).get_queryset()

        return queryset.filter(created_at__gt=oldest)
