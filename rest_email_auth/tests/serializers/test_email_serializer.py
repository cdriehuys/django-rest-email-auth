try:
    from unittest import mock
except ImportError:
    import mock

from rest_email_auth import serializers


@mock.patch(
    'rest_email_auth.serializers.models.EmailAddress.send_confirmation',
    autospec=True)
def test_create(mock_send_confirmation, user_factory):
    """
    Test creating a new email address from the serializer.

    Creating a new email address should also send a confirmation email
    for the provided address.
    """
    user = user_factory()
    data = {
        'email': 'test@example.com',
    }

    serializer = serializers.EmailSerializer(data=data)
    assert serializer.is_valid()

    email = serializer.save(user=user)

    assert email.email == data['email']

    # Make sure a confirmation email was sent
    assert mock_send_confirmation.call_count == 1


@mock.patch(
    'rest_email_auth.serializers.models.EmailAddress.send_duplicate_notification',  # noqa
    autospec=True)
def test_create_duplicate(
        mock_duplicate_notification,
        email_factory,
        user_factory):
    """
    Attempting to add an email address that already exists should send a
    notification to the existing email.
    """
    email = email_factory()
    user = user_factory()

    data = {
        'email': email.email,
    }

    serializer = serializers.EmailSerializer(data=data)
    assert serializer.is_valid(), serializer.errors

    serializer.save(user=user)

    assert mock_duplicate_notification.call_count == 1
    assert mock_duplicate_notification.call_args[0] == (email,)


def test_serialize(email_factory):
    """
    Test serializing an email address.
    """
    email = email_factory()
    serializer = serializers.EmailSerializer(email)

    expected = {
        'id': email.id,
        'created_at': email.created_at.isoformat(),
        'email': email.email,
        'is_verified': email.is_verified,
    }

    assert serializer.data == expected


def test_validate_changed_email(email_factory):
    """
    If a bound serializer attempts to change the email address of its
    instance it should not be valid.
    """
    email = email_factory(email='old@example.com')
    data = {
        'email': 'new@example.com',
    }

    serializer = serializers.EmailSerializer(email, data=data)

    assert not serializer.is_valid()
    assert set(serializer.errors.keys()) == {'email'}
