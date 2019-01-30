try:
    from unittest import mock
except ImportError:
    import mock

from rest_email_auth import models, serializers


def test_save(password_reset_token_factory):
    """
    Saving the serializer with a valid token and password should reset
    the associated user's password.
    """
    token = password_reset_token_factory()
    user = token.email.user

    data = {"key": token.key, "password": "new_passw0rd"}

    serializer = serializers.PasswordResetSerializer(data=data)
    assert serializer.is_valid()

    serializer.save()
    user.refresh_from_db()

    assert user.check_password(data["password"])
    assert models.PasswordResetToken.objects.count() == 0


def test_validate_key_expired(password_reset_token_factory):
    """
    If the key provided corresponds to a token that has expired, the
    serializer should not validate.
    """
    token = password_reset_token_factory()
    data = {"key": token.key, "password": "new_passw0rd"}

    serializer = serializers.PasswordResetSerializer(data=data)

    with mock.patch(
        "rest_email_auth.serializers.models.PasswordResetToken.valid_tokens.filter",  # noqa
        return_value=models.PasswordResetToken.objects.none(),
    ) as mock_filter:  # noqa
        assert not serializer.is_valid()

    assert set(serializer.errors.keys()) == {"key"}
    assert mock_filter.call_count == 1


def test_validate_key_invalid(db):
    """
    If there is no reset token with the provided key, the serializer
    should not validate.
    """
    data = {
        "key": "00000000-0000-0000-0000-000000000000",
        "password": "new_passw0rd",
    }

    serializer = serializers.PasswordResetSerializer(data=data)

    assert not serializer.is_valid()
    assert set(serializer.errors.keys()) == {"key"}


@mock.patch(
    "rest_email_auth.serializers.password_validation.validate_password",
    autospec=True,
)
def test_validate_password(mock_validate_password):
    """
    The serializer should pass the provided password through Django's
    password validation system.
    """
    data = {"key": "foo", "password": "foobar"}
    serializer = serializers.PasswordResetSerializer(data=data)

    serializer.is_valid()

    assert mock_validate_password.call_count == 1
    assert mock_validate_password.call_args[0] == (data["password"],)
