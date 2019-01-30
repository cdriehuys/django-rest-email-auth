"""
Fixtures for testing authentication backends.
"""

import pytest

from rest_email_auth import authentication


@pytest.fixture(scope="session")
def base_auth_backend():
    """
    Return an instance of the base authentication backend.
    """
    return authentication.BaseBackend()


@pytest.fixture(scope="session")
def verified_email_auth_backend():
    """
    Return an instance of the authentication backend that only accepts
    verified emails.
    """
    return authentication.VerifiedEmailBackend()
