"""Fixtures used to test the ``rest_email_auth`` app.
"""

import copy
import logging

try:
    from unittest import mock
except ImportError:
    import mock

import pytest

from rest_framework.test import APIClient, APIRequestFactory

from rest_email_auth import (
    app_settings as application_settings,
    factories,
    signals,
)


logger = logging.getLogger(__name__)


class MutableAppSettings(object):
    """
    A mutable version of the application's settings.
    """

    def __init__(self, settings_obj):
        """
        Create a new mutable settings instance.

        This is done by making a copy of the REST_EMAIL_AUTH
        configuration dictionary. Since the settings fixture is rolled
        back at the end of each test, it sees that we changed the
        dictionary reference and points it back to the original.

        Args:
            settings_obj:
                The object through which Django's settings are
                accessible. We rely on the fact that this object is
                rolled back after each test.
        """
        settings_obj.REST_EMAIL_AUTH = copy.deepcopy(
            settings_obj.REST_EMAIL_AUTH
        )

        # Since we pass __setattr__ through to the settings dictionary
        # we have to set attributes by modifying the instance's __dict__
        # directly.
        self.__dict__["settings_obj"] = settings_obj
        self.__dict__["original"] = copy.deepcopy(settings_obj.REST_EMAIL_AUTH)

    def __getattr__(self, name):
        """
        Attempt to lookup attributes using the application's settings.

        If the attribute is not accessible through the application
        settings it falls back to the default behavior.
        """
        if hasattr(application_settings, name):
            return getattr(application_settings, name)

        return super(MutableAppSettings, self).__getattribute__(name)

    def __setattr__(self, name, value):
        """
        Setting attributes modifies the settings dictionary directly.
        """
        self.settings_obj.REST_EMAIL_AUTH[name] = value


@pytest.fixture
def api_client():
    """
    Fixture to get a client for making API requests.

    Returns:
        An instance of the APIClient provided by DRF.
    """
    return APIClient()


@pytest.fixture
def api_rf():
    """
    Fixture to get a factory for creating API requests.

    Returns:
        An instance of the request factory provided by DRF.
    """
    return APIRequestFactory()


@pytest.fixture
def app_settings(settings):
    """
    Fixture to get a mutable copy of the application's settings.

    Any changes are rolled back at the end of the test.
    """
    return MutableAppSettings(settings)


@pytest.fixture
def email_confirmation_factory(db):
    """
    Fixture to get the factory used to create email confirmations.

    Returns:
        The factory used to create ``EmailConfirmation`` instances.
    """
    return factories.EmailConfirmationFactory


@pytest.fixture
def email_factory(db):
    """
    Fixture to get the factory used to create email addresses.

    Returns:
        The factory used to create ``EmailAddress`` instances.
    """
    return factories.EmailFactory


@pytest.fixture
def email_verification_listener():
    """
    Fixture to get a listener for the 'email_verified' signal.
    """
    listener = mock.Mock(name="Mock Email Verification Listener")
    signals.email_verified.connect(listener)

    yield listener

    signals.email_verified.disconnect(listener)


@pytest.fixture
def password_reset_token_factory(db):
    """
    Fixture to get the factory usedd to create password reset tokens.

    Returns:
        The factory used to create ``PasswordResetToken`` instances.
    """
    return factories.PasswordResetTokenFactory


@pytest.fixture
def registration_listener():
    """
    Fixture to get a listener for the 'user_registered' signal.
    """
    listener = mock.Mock(name="Mock Registration Listener")
    signals.user_registered.connect(listener)

    yield listener

    signals.user_registered.disconnect(listener)


@pytest.fixture
def user_factory(db):
    """
    Fixture to get the factory used to create users.

    Returns:
        The factory used to create Django user instances.
    """
    return factories.UserFactory
