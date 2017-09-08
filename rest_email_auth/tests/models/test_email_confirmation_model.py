import datetime
from unittest import mock

from rest_email_auth import models


def test_confirm(email_confirmation_factory, email_factory):
    """
    Confirming a confirmation should mark the associated email address
    as verified.
    """
    email = email_factory()
    confirmation = email_confirmation_factory(email=email)

    confirmation.confirm()
    email.refresh_from_db()

    assert email.is_verified


def test_create_email_confirmation(email_factory):
    """
    Test creating a new email confirmation.
    """
    models.EmailConfirmation.objects.create(
        email=email_factory())


def test_is_expired(email_confirmation_factory):
    """
    If it has been more than a day since the confirmation was created it
    should be marked as expired.
    """
    confirmation = email_confirmation_factory()
    future_time = confirmation.created_at + datetime.timedelta(days=2)

    with mock.patch(
            'rest_email_auth.models.timezone.now',
            autospec=True,
            return_value=future_time):
        assert confirmation.is_expired


def test_is_expired_unexpired(email_confirmation_factory):
    """
    If it has been less than a day since the confirmation was created it
    should not be marked as expired.
    """
    confirmation = email_confirmation_factory()

    assert not confirmation.is_expired
