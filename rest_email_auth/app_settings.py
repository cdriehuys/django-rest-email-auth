"""
Settings specific to the application.

The setting implementation is modeled off of "Django Allauth's" from:
https://github.com/pennersr/django-allauth/blob/master/allauth/account/app_settings.py
"""


class AppSettings(object):

    def __init__(self):
        """
        Perform some basic settings checks.
        """
        # The user must provide a URL template for the verification
        # endpoint.
        assert self.EMAIL_VERIFICATION_URL

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

        settings_dict = getattr(settings, 'REST_EMAIL_AUTH', {})

        return settings_dict.get(name, default)

    @property
    def CONFIRMATION_EXPIRATION(self):
        """
        The duration that an email confirmation is valid for.

        Defaults to 1 day.
        """
        import datetime

        return self._setting(
            'CONFIRMATION_EXPIRATION',
            datetime.timedelta(days=1))

    @property
    def CONFIRMATION_SAVE_PERIOD(self):
        """
        The duration that expired confirmations are saved for.

        Defaults to 7 days.
        """
        import datetime

        return self._setting(
            'CONFIRMATION_SAVE_PERIOD',
            datetime.timedelta(days=7))

    @property
    def EMAIL_VERIFICATION_URL(self):
        """
        The template to use for the email verification url.
        """
        return self._setting('EMAIL_VERIFICATION_URL', '')


# Ugly? Guido recommends this himself ...
# http://mail.python.org/pipermail/python-ideas/2012-May/014969.html
import sys      # noqa


app_settings = AppSettings()
app_settings.__name__ = __name__
sys.modules[__name__] = app_settings
