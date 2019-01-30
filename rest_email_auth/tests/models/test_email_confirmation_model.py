import datetime

try:
    from unittest import mock
except ImportError:
    import mock

from rest_email_auth import models


def test_confirm(
    email_confirmation_factory, email_factory, email_verification_listener
):
    """
    Confirming a confirmation should mark the associated email address
    as verified.
    """
    email = email_factory()
    confirmation = email_confirmation_factory(email=email)

    confirmation.confirm()
    email.refresh_from_db()

    assert email.is_verified
    assert email_verification_listener.call_count == 1
    assert (
        email_verification_listener.call_args[1]["sender"]
        == confirmation.__class__
    )
    assert email_verification_listener.call_args[1]["email"] == email


def test_create_email_confirmation(email_factory):
    """
    Test creating a new email confirmation.
    """
    models.EmailConfirmation.objects.create(email=email_factory())


def test_is_expired(email_confirmation_factory):
    """
    If it has been more than a day since the confirmation was created it
    should be marked as expired.
    """
    confirmation = email_confirmation_factory()
    future_time = confirmation.created_at + datetime.timedelta(days=2)

    with mock.patch(
        "rest_email_auth.models.timezone.now",
        autospec=True,
        return_value=future_time,
    ):
        assert confirmation.is_expired


def test_is_expired_unexpired(email_confirmation_factory):
    """
    If it has been less than a day since the confirmation was created it
    should not be marked as expired.
    """
    confirmation = email_confirmation_factory()

    assert not confirmation.is_expired


@mock.patch("rest_email_auth.models.email_utils.send_email")
def test_send(mock_send_email, email_confirmation_factory, settings):
    """
    Sending the confirmation should send an email to the associated
    email address.
    """
    settings.REST_EMAIL_AUTH = {
        "EMAIL_VERIFICATION_URL": "https://example.com/verify?key={key}"
    }

    confirmation = email_confirmation_factory()
    confirmation.send()

    url = settings.REST_EMAIL_AUTH["EMAIL_VERIFICATION_URL"].format(
        key=confirmation.key
    )

    context = {"verification_url": url}

    assert mock_send_email.call_count == 1
    assert mock_send_email.call_args[1] == {
        "context": context,
        "from_email": settings.DEFAULT_FROM_EMAIL,
        "recipient_list": [confirmation.email.email],
        "subject": "Please Verify Your Email Address",
        "template_name": "rest_email_auth/emails/verify-email",
    }
