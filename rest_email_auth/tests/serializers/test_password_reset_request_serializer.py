try:
    from unittest import mock
except ImportError:
    import mock

from rest_email_auth import models, serializers


@mock.patch(
    "rest_email_auth.serializers.models.PasswordResetToken.send", autospec=True
)
def test_save(mock_send_reset, email_factory):
    """
    Saving a serializer with valid data should send out a password reset
    email.
    """
    email = email_factory(is_verified=True)
    data = {"email": email.email}

    serializer = serializers.PasswordResetRequestSerializer(data=data)
    assert serializer.is_valid()

    token = serializer.save()

    # Saving the serializer should not modify its data
    assert serializer.data == data

    assert token.email == email
    assert token.send.call_count == 1


def test_save_nonexistent_email(db):
    """
    If a non-existent email address is provided to the reset endpoint,
    no action should be taken.
    """
    data = {"email": "fake@example.com"}

    serializer = serializers.PasswordResetRequestSerializer(data=data)
    assert serializer.is_valid()

    token = serializer.save()

    assert token is None
    assert models.PasswordResetToken.objects.count() == 0


def test_save_unverified_email(email_factory):
    """
    If the provided email address has not been verified yet, no action
    should be taken.
    """
    email = email_factory(is_verified=False)
    data = {"email": email.email}

    serializer = serializers.PasswordResetRequestSerializer(data=data)
    assert serializer.is_valid()

    token = serializer.save()

    assert token is None
    assert models.PasswordResetToken.objects.count() == 0
