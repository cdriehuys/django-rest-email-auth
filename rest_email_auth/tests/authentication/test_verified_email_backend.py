"""
Tests for the verified email backend.
"""


def test_authenticate(
    email_factory, user_factory, verified_email_auth_backend
):
    """
    Passing in a verified email address and the user's password should
    successfully authenticate the user.
    """
    user = user_factory(password="password")
    email = email_factory(is_verified=True, user=user)

    assert (
        verified_email_auth_backend.authenticate(
            email=email.email, password="password", request=None
        )
        == user
    )


def test_authenticate_invalid_password(
    email_factory, user_factory, verified_email_auth_backend
):
    """
    Providing the wrong password should cause ``None`` to be returned.
    """
    user = user_factory(password="password")
    email = email_factory(is_verified=True, user=user)

    assert (
        verified_email_auth_backend.authenticate(
            email=email.email, password="notpassword", request=None
        )
        is None
    )


def test_authenticate_missing_email(user_factory, verified_email_auth_backend):
    """
    If the provided email doesn't exist in the system, ``None`` should
    be returned.
    """
    user_factory(password="password")

    assert (
        verified_email_auth_backend.authenticate(
            email="missing@example.com", password="password", request=None
        )
        is None
    )


def test_authenticate_unverified_email(
    email_factory, user_factory, verified_email_auth_backend
):
    """
    If the provided email address exists but has not been verified yet
    ``None`` should be returned.
    """
    user = user_factory(password="password")
    email = email_factory(is_verified=False, user=user)

    assert (
        verified_email_auth_backend.authenticate(
            email=email.email, password="password", request=None
        )
        is None
    )


def test_authenticate_username(
    email_factory, user_factory, verified_email_auth_backend
):
    """
    The ``username`` parameter should act as an alias for the ``email``
    parameter.
    """
    user = user_factory(password="password")
    email = email_factory(is_verified=True, user=user)

    assert (
        verified_email_auth_backend.authenticate(
            password="password", request=None, username=email.email
        )
        == user
    )
