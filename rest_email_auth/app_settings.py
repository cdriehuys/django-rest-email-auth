"""
Settings specific to the application.

The setting implementation is modeled off of "Django Allauth's" from:
https://github.com/pennersr/django-allauth/blob/master/allauth/account/app_settings.py
"""

import sys

from django.utils.translation import gettext_lazy as _


class AppSettings(object):
    def __init__(self):
        """
        Perform some basic settings checks.
        """
        # The user must provide a URL template for the verification
        # and password reset endpoints.
        assert self.EMAIL_VERIFICATION_URL
        assert self.PASSWORD_RESET_URL

    def _setting(self, name, default):
        """
        Retrieve a setting from the current Django settings.

        Settings are retrieved from the ``REST_EMAIL_AUTH`` dict in the
        settings file.

        Args:
            name (str):
                The name of the setting to retrieve.
            default:
                The setting's default value.

        Returns:
            The value provided in the settings dictionary if it exists.
            The default value is returned otherwise.
        """
        from django.conf import settings

        settings_dict = getattr(settings, "REST_EMAIL_AUTH", {})

        return settings_dict.get(name, default)

    @property
    def CONFIRMATION_EXPIRATION(self):
        """
        The duration that an email confirmation is valid for.

        Defaults to 1 day.
        """
        import datetime

        return self._setting(
            "CONFIRMATION_EXPIRATION", datetime.timedelta(days=1)
        )

    @property
    def CONFIRMATION_SAVE_PERIOD(self):
        """
        The duration that expired confirmations are saved for.

        Defaults to 7 days.
        """
        import datetime

        return self._setting(
            "CONFIRMATION_SAVE_PERIOD", datetime.timedelta(days=7)
        )

    @property
    def EMAIL_SUBJECT_DUPLICATE(self):
        """
        The subject to use for emails notifying users of a duplicate
        registration attempt.
        """
        return self._setting(
            "EMAIL_SUBJECT_DUPLICATE", _("Registration Attempt")
        )

    @property
    def EMAIL_SUBJECT_VERIFICATION(self):
        """
        The subject to use for emails containing verification tokens.
        """
        return self._setting(
            "EMAIL_SUBJECT_VERIFICATION", _("Please Verify Your Email Address")
        )

    @property
    def EMAIL_VERIFICATION_PASSWORD_REQUIRED(self):
        """
        A boolean indicating if the user's password is required to
        verify their email address.
        """
        return self._setting("EMAIL_VERIFICATION_PASSWORD_REQUIRED", True)

    @property
    def EMAIL_VERIFICATION_URL(self):
        """
        The template to use for the email verification url.
        """
        return self._setting("EMAIL_VERIFICATION_URL", "")

    @property
    def PASSWORD_RESET_EXPIRATION(self):
        """
        The duration that a password reset token is valid for.

        Defaults to 1 hour.
        """
        import datetime

        return self._setting(
            "PASSWORD_RESET_EXPIRATION", datetime.timedelta(hours=1)
        )

    @property
    def PASSWORD_RESET_URL(self):
        """
        The template to use for the password reset url.
        """
        return self._setting("PASSWORD_RESET_URL", "")

    @property
    def REGISTRATION_SERIALIZER(self):
        """
        The serializer class used for registering new users.
        """
        from django.utils.module_loading import import_string

        return import_string(
            self._setting(
                "REGISTRATION_SERIALIZER",
                "rest_email_auth.serializers.RegistrationSerializer",
            )
        )

    @property
    def PATH_TO_RESET_EMAIL_TEMPLATE(self):
        """
        The path to the email template used for
        resetting a password.
        Defaults to the default template.
        """

        return self._setting(
            "PATH_TO_RESET_EMAIL_TEMPLATE",
            "rest_email_auth/emails/reset-password",
        )

    @property
    def PATH_TO_VERIFY_EMAIL_TEMPLATE(self):
        """
        The path to the email template used for
        verifying an email.
        Defaults to the default template.
        """

        return self._setting(
            "PATH_TO_VERIFY_EMAIL_TEMPLATE",
            "rest_email_auth/emails/verify-email",
        )

    @property
    def PATH_TO_DUPLICATE_EMAIL_TEMPLATE(self):
        """
        The path to the email template used for
        notifying about a duplicate signup.
        Defaults to the default template.
        """

        return self._setting(
            "PATH_TO_DUPLICATE_EMAIL_TEMPLATE",
            "rest_email_auth/emails/duplicate-email",
        )


# Ugly? Guido recommends this himself ...
# http://mail.python.org/pipermail/python-ideas/2012-May/014969.html

app_settings = AppSettings()
app_settings.__name__ = __name__
sys.modules[__name__] = app_settings
