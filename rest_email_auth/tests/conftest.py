"""Fixtures used to test the ``rest_email_auth`` app.
"""

import pytest

from rest_email_auth import factories


@pytest.fixture
def user_factory(db):
    """
    Fixture to get the factory used to create users.

    Returns:
        The factory used to create Django user instances.
    """
    return factories.UserFactory
