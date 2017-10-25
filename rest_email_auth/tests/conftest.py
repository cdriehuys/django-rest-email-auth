"""Fixtures used to test the ``rest_email_auth`` app.
"""

import pytest

from rest_framework.test import APIClient, APIRequestFactory

from rest_email_auth import factories


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
def user_factory(db):
    """
    Fixture to get the factory used to create users.

    Returns:
        The factory used to create Django user instances.
    """
    return factories.UserFactory
