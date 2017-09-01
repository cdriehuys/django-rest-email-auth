from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


class EmailAddress(models.Model):
    """
    A user's email address.
    """
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('created at'))

    email = models.EmailField(
        max_length=255,
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
