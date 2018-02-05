import datetime

from django.template.loader import render_to_string

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


# For some reason, if 'mailoutbox' is listed before
# 'password_reset_token_factory', the test breaks.
def test_send(password_reset_token_factory, mailoutbox, settings):
    """
    Sending the token should send an email to the address associated
    with the token.
    """
    settings.REST_EMAIL_AUTH = {
        'PASSWORD_RESET_URL': 'https://example.com/reset/{key}',
    }

    token = password_reset_token_factory()
    token.send()

    url = settings.REST_EMAIL_AUTH['PASSWORD_RESET_URL'].format(
        key=token.key)

    context = {
        'reset_url': url,
    }
    expected_content = render_to_string(
        context=context,
        template_name='rest_email_auth/emails/reset-password.txt')

    assert len(mailoutbox) == 1

    msg = mailoutbox[0]

    assert msg.body == expected_content
    assert msg.from_email == settings.DEFAULT_FROM_EMAIL
    assert msg.subject == 'Reset Your Password'
    assert msg.to == [token.email.email]


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
