try:
    from unittest import mock
except ImportError:
    import mock

import pytest

from rest_email_auth import serializers


@pytest.mark.django_db
def test_create_new_user():
    """
    Saving a serializer with valid data should create a new user.
    """
    data = {
        'email': 'test@example.com',
        'password': 'password',
        'username': 'user',
    }

    serializer = serializers.RegistrationSerializer(data=data)
    assert serializer.is_valid()

    with mock.patch(
            'rest_email_auth.serializers.models.EmailAddress.send_confirmation',    # noqa
            autospec=True) as mock_send_confirmation:
        user = serializer.save()

    assert user.username == data['username']
    assert user.check_password(data['password'])
    assert user.email_addresses.count() == 1

    email = user.email_addresses.get()

    assert email.email == data['email']

    # Make sure we sent out an email confirmation
    assert mock_send_confirmation.call_count == 1
