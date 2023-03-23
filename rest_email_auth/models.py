import datetime
import logging
import uuid

from django.conf import settings
from django.db import models, transaction
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _

import email_utils

from rest_email_auth import app_settings, managers, signals


logger = logging.getLogger(__name__)


def generate_token():
    """
    Get a random 64 character string.

    Returns:
        str:
            A random 64 character string.
    """
    return get_random_string(length=64)


class EmailAddress(models.Model):
    """
    A user's email address.
    """

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("created at")
    )
    email = models.EmailField(
        max_length=255, unique=True, verbose_name=_("email")
    )
    is_primary = models.BooleanField(
        default=False,
        help_text=_(
            "Boolean indicating if the email is the user's primary " "address."
        ),
        verbose_name=_("is primary"),
    )
    is_verified = models.BooleanField(
        default=False,
        help_text=_(
            "Boolean indicating if the user has verified ownership of "
            "the email address."
        ),
        verbose_name=_("is verified"),
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="email_addresses",
        related_query_name="email_address",
        verbose_name=_("user"),
    )

    # Use custom manager
    objects = managers.EmailAddressManager()

    class Meta(object):
        verbose_name = _("email address")
        verbose_name_plural = _("email addresses")

    def __str__(self):
        """
        Get a string representation of the email address.

        Returns:
            str:
                A text version of the email address. Ex:
                ``test@example.com``.
        """
        return self.email

    def send_confirmation(self):
        """
        Send a verification email for the email address.
        """
        confirmation = EmailConfirmation.objects.create(email=self)
        confirmation.send()

    def send_duplicate_notification(self):
        """
        Send a notification about a duplicate signup.
        """
        email_utils.send_email(
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[self.email],
            subject=app_settings.EMAIL_SUBJECT_DUPLICATE,
            template_name=app_settings.PATH_TO_DUPLICATE_EMAIL_TEMPLATE,
        )

        logger.info("Sent duplicate email notification to: %s", self.email)

    def set_primary(self):
        """
        Set this email address as the user's primary email.
        """
        query = EmailAddress.objects.filter(is_primary=True, user=self.user)
        query = query.exclude(pk=self.pk)

        # The transaction is atomic so there is never a gap where a user
        # has no primary email address.
        with transaction.atomic():
            query.update(is_primary=False)

            self.is_primary = True
            self.save()

        logger.info(
            "Set %s as the primary email address for %s.",
            self.email,
            self.user,
        )


class EmailConfirmation(models.Model):
    """
    Model to store a token used to verify an email address.
    """

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("created at")
    )
    email = models.ForeignKey(
        "rest_email_auth.EmailAddress",
        on_delete=models.CASCADE,
        related_name="confirmations",
        related_query_name="confirmation",
        verbose_name=_("email"),
    )
    key = models.CharField(
        default=generate_token,
        editable=False,
        max_length=255,
        verbose_name=_("confirmation key"),
    )

    class Meta(object):
        verbose_name = _("email confirmation")
        verbose_name_plural = _("email confirmations")

    def confirm(self):
        """
        Mark the instance's email as verified.
        """
        self.email.is_verified = True
        self.email.save()

        signals.email_verified.send(email=self.email, sender=self.__class__)

        logger.info("Verified email address: %s", self.email.email)

    @property
    def is_expired(self):
        """
        Determine if the confirmation has expired.

        Returns:
            bool:
                ``True`` if the confirmation has expired and ``False``
                otherwise.
        """
        expiration_time = self.created_at + datetime.timedelta(days=1)

        return timezone.now() > expiration_time

    def send(self):
        """
        Send a verification email to the user.
        """
        context = {
            "verification_url": app_settings.EMAIL_VERIFICATION_URL.format(
                key=self.key
            )
        }

        email_utils.send_email(
            context=context,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[self.email.email],
            subject=app_settings.EMAIL_SUBJECT_VERIFICATION,
            template_name=app_settings.PATH_TO_VERIFY_EMAIL_TEMPLATE,
        )

        logger.info(
            "Sent confirmation email to %s for user #%d",
            self.email.email,
            self.email.user.id,
        )


class PasswordResetToken(models.Model):
    """
    Store a token that can be used to reset a user's password.
    """

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text=_("The time at which the password reset token was created."),
        verbose_name=_("created at"),
    )
    email = models.ForeignKey(
        "rest_email_auth.EmailAddress",
        editable=False,
        help_text=_("The email address used to request the password reset."),
        on_delete=models.CASCADE,
        related_name="password_reset_tokens",
        related_query_name="password_reset_token",
        verbose_name=_("email address"),
    )
    key = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        help_text=_(
            "The token that authorizes the user to reset their " "password."
        ),
        verbose_name=_("key"),
    )

    # Custom managers. We have to explicitly define the default manager
    # so that it doesn't get overwritten.
    objects = models.Manager()
    valid_tokens = managers.ValidPasswordResetTokenManager()

    class Meta:
        verbose_name = _("password reset token")
        verbose_name_plural = _("password reset tokens")

    def __str__(self):
        """
        Get a string representation of the instance.

        Returns:
            Information about the token's owner.
        """
        return "Password reset token for '{}'".format(self.email.user)

    def send(self):
        """
        Send the password reset token to the user.
        """
        context = {
            "reset_url": app_settings.PASSWORD_RESET_URL.format(key=self.key)
        }

        email_utils.send_email(
            context=context,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[self.email.email],
            subject=_("Reset Your Password"),
            template_name=app_settings.PATH_TO_RESET_EMAIL_TEMPLATE,
        )

        logger.info("Sent password reset email to %s", self.email)
