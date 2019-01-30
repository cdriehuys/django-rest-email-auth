import datetime

try:
    from unittest import mock
except ImportError:
    import mock

from rest_email_auth import models


def test_create(email_factory):
    """
    Test creating a new password reset token.
    """
    models.PasswordResetToken.objects.create(email=email_factory())


def test_string_conversion(password_reset_token_factory):
    """
    Converting a password reset token to a string should return
    information about the token's owner.
    """
    token = password_reset_token_factory()
    expected = "Password reset token for '{}'".format(token.email.user)

    assert str(token) == expected


@mock.patch("rest_email_auth.models.email_utils.send_email")
def test_send(mock_send_email, password_reset_token_factory, settings):
    """
    Sending the token should send an email to the address associated
    with the token.
    """
    settings.REST_EMAIL_AUTH = {
        "PASSWORD_RESET_URL": "https://example.com/reset/{key}"
    }

    token = password_reset_token_factory()
    token.send()

    url = settings.REST_EMAIL_AUTH["PASSWORD_RESET_URL"].format(key=token.key)

    context = {"reset_url": url}

    assert mock_send_email.call_count == 1
    assert mock_send_email.call_args[1] == {
        "context": context,
        "from_email": settings.DEFAULT_FROM_EMAIL,
        "recipient_list": [token.email.email],
        "subject": "Reset Your Password",
        "template_name": "rest_email_auth/emails/reset-password",
    }


def test_valid_tokens(password_reset_token_factory, app_settings):
    """
    The valid tokens queryset should include unexpired tokens.
    """
    app_settings.PASSWORD_RESET_EXPIRATION = datetime.timedelta(hours=1)

    token = password_reset_token_factory()

    assert list(models.PasswordResetToken.valid_tokens.all()) == [token]


def test_valid_tokens_expired(password_reset_token_factory, app_settings):
    """
    The valid tokens queryset should not include expired tokens.
    """
    app_settings.PASSWORD_RESET_EXPIRATION = datetime.timedelta()

    password_reset_token_factory()

    assert not models.PasswordResetToken.valid_tokens.exists()
