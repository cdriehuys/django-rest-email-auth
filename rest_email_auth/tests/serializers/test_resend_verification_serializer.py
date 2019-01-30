try:
    from unittest import mock
except ImportError:
    import mock

from rest_email_auth import serializers


@mock.patch(
    "rest_email_auth.serializers.models.EmailAddress.send_confirmation",
    autospec=True,
)
def test_save(mock_send_confirmation, email_factory):
    """
    Saving the serializer should send a new confirmation.
    """
    email = email_factory()

    data = {"email": email.email}

    serializer = serializers.ResendVerificationSerializer(data=data)
    assert serializer.is_valid()

    serializer.save()

    assert mock_send_confirmation.call_count == 1


@mock.patch(
    "rest_email_auth.serializers.models.EmailAddress.send_confirmation",
    autospec=True,
)
def test_save_nonexistent_email(mock_send_confirmation, db):
    """
    If the provided email address is not in the database, no action
    should be taken.
    """
    data = {"email": "test@example.com"}

    serializer = serializers.ResendVerificationSerializer(data=data)
    assert serializer.is_valid()

    serializer.save()

    assert mock_send_confirmation.call_count == 0


@mock.patch(
    "rest_email_auth.serializers.models.EmailAddress.send_confirmation",
    autospec=True,
)
def test_save_verified_email(mock_send_confirmation, email_factory):
    """
    If the provided email has already been verified, no action should be
    taken.
    """
    email = email_factory(is_verified=True)

    data = {"email": email.email}

    serializer = serializers.ResendVerificationSerializer(data=data)
    assert serializer.is_valid()

    serializer.save()

    assert mock_send_confirmation.call_count == 0
