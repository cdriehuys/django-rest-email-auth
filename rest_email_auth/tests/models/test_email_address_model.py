try:
    from unittest import mock
except ImportError:
    import mock

from rest_email_auth import models


def test_create(user_factory):
    """
    Test creating an email address.
    """
    email = models.EmailAddress.objects.create(
        email='test@example.com',
        user=user_factory())

    assert not email.is_verified


def test_send_confirmation(email_factory):
    """
    Sending a confirmation should create an ``EmailConfirmation``
    instance and send a verification email.
    """
    email = email_factory()

    with mock.patch(
            'rest_email_auth.models.EmailConfirmation.send',
            autospec=True) as mock_send:
        email.send_confirmation()

    assert email.confirmations.count() == 1
    assert mock_send.call_count == 1


def test_string_conversion(email_factory):
    """
    Converting an email address to a string should return the email
    address.
    """
    email = email_factory()

    assert str(email) == email.email
