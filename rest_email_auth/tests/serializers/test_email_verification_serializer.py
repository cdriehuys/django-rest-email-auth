try:
    from unittest import mock
except ImportError:
    import mock

from rest_email_auth import serializers


def test_confirm_email(
    email_confirmation_factory, email_factory, user_factory
):
    """
    If a valid confirmation key and password are provided, the email
    matching the key should be verified.
    """
    user = user_factory(password="password")
    email = email_factory(user=user)
    confirmation = email_confirmation_factory(email=email)

    data = {"key": confirmation.key, "password": "password"}

    serializer = serializers.EmailVerificationSerializer(data=data)
    assert serializer.is_valid()

    serializer.save()
    email.refresh_from_db()

    expected = {"email": email.email}

    assert serializer.data == expected
    assert email.is_verified
    assert email.confirmations.count() == 0


def test_validate_expired(email_confirmation_factory):
    """
    If the confirmation matching the provided key is expired, the
    serializer should not be valid.
    """
    confirmation = email_confirmation_factory()

    data = {"key": confirmation.key, "password": "password"}

    serializer = serializers.EmailVerificationSerializer(data=data)

    with mock.patch(
        "rest_email_auth.serializers.models.EmailConfirmation.is_expired",
        new_callable=mock.PropertyMock,
    ) as mock_is_expired:
        mock_is_expired.return_value = True

        assert not serializer.is_valid()

    assert mock_is_expired.call_count == 1
    assert set(serializer.errors.keys()) == {"key"}


def test_validate_invalid_key(db):
    """
    If there is no confirmation with the provided key, the serializer
    should not be valid.
    """
    data = {"key": "invalid", "password": "password"}

    serializer = serializers.EmailVerificationSerializer(data=data)

    assert not serializer.is_valid()
    assert set(serializer.errors.keys()) == {"key"}


def test_validate_invalid_password(
    email_confirmation_factory, email_factory, user_factory
):
    """
    If an invalid password is provided, the serializer should not be
    valid.
    """
    user = user_factory(password="password")
    email = email_factory(user=user)
    confirmation = email_confirmation_factory(email=email)

    data = {"key": confirmation.key, "password": "notpassword"}

    serializer = serializers.EmailVerificationSerializer(data=data)

    assert not serializer.is_valid()
    assert set(serializer.errors.keys()) == {"non_field_errors"}


def test_validate_no_password(
    app_settings, email_confirmation_factory, email_factory, user_factory
):
    """
    If the password requirement for verifying email addresses is
    disabled then users should be able to verify email addresses without
    providing their password.
    """
    app_settings.EMAIL_VERIFICATION_PASSWORD_REQUIRED = False

    user = user_factory()
    email = email_factory(user=user)
    confirmation = email_confirmation_factory(email=email)

    data = {"key": confirmation.key}

    serializer = serializers.EmailVerificationSerializer(data=data)
    assert serializer.is_valid()

    serializer.save()
    email.refresh_from_db()

    expected = {"email": email.email}

    assert serializer.data == expected
    assert email.is_verified
    assert email.confirmations.count() == 0
