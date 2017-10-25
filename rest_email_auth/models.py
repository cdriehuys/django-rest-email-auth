import datetime
import logging

from django.conf import settings
from django.core import mail
from django.db import models
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.translation import ugettext_lazy as _

from rest_email_auth import app_settings


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
        auto_now_add=True,
        verbose_name=_('created at'))

    email = models.EmailField(
        max_length=255,
        unique=True,
        verbose_name=_('email'))
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='email_addresses',
        related_query_name='email_address',
        verbose_name=_('user'))

    is_verified = models.BooleanField(
        default=False,
        help_text=_('Boolean indicating if the user has verified ownership of '
                    'the email address.'),
        verbose_name=_('is verified'))

    class Meta(object):
        verbose_name = _('email address')
        verbose_name_plural = _('email addresses')

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

    def send_duplicate_signup(self):
        """
        Send a notification about a duplicate signup.
        """
        context = {}
        message = render_to_string(
            context=context,
            template_name='rest_email_auth/emails/duplicate-signup.txt')

        mail.send_mail(
            from_email=None,
            message=message,
            recipient_list=[self.email],
            subject=_('Registration Attempt'))

        logger.info('Sent duplicate signup notification to: %s', self.email)


class EmailConfirmation(models.Model):
    """
    Model to store a token used to verify an email address.
    """
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('created at'))
    email = models.ForeignKey(
        'rest_email_auth.EmailAddress',
        on_delete=models.CASCADE,
        related_name='confirmations',
        related_query_name='confirmation',
        verbose_name=_('email'))
    key = models.CharField(
        default=generate_token,
        editable=False,
        max_length=255,
        verbose_name=_('confirmation key'))

    class Meta(object):
        verbose_name = _('email confirmation')
        verbose_name_plural = _('email confirmations')

    def confirm(self):
        """
        Mark the instance's email as verified.
        """
        self.email.is_verified = True
        self.email.save()

        logger.info('Verified email address: %s', self.email.email)

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
            'verification_url': app_settings.EMAIL_VERIFICATION_URL.format(
                key=self.key),
        }
        message = render_to_string(
            context=context,
            template_name='rest_email_auth/emails/verify-email.txt')

        mail.send_mail(
            from_email=None,
            message=message,
            recipient_list=[self.email.email],
            subject=_('Please Verify Your Email Address'))
