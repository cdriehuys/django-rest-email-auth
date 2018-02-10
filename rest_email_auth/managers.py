from django.db import models
from django.utils import timezone

from rest_email_auth import app_settings


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
