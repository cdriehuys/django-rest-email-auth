try:
    from unittest import mock
except ImportError:
    import mock

from django.conf import settings
from django.template.loader import render_to_string

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


def test_send_duplicate_signup(email_factory, mailoutbox):
    """
    Sending a duplicate signup notification should send the user an
    email stating that their email was used to register even though
    they already have an account.
    """
    email = email_factory()
    email.send_duplicate_signup()

    context = {}
    message = render_to_string(
        context=context,
        template_name='rest_email_auth/emails/duplicate-signup.txt')

    assert len(mailoutbox) == 1

    msg = mailoutbox[0]

    assert msg.body == message
    assert msg.from_email == settings.DEFAULT_FROM_EMAIL
    assert msg.subject == 'Registration Attempt'
    assert msg.to == [email.email]


def test_string_conversion(email_factory):
    """
    Converting an email address to a string should return the email
    address.
    """
    email = email_factory()

    assert str(email) == email.email
