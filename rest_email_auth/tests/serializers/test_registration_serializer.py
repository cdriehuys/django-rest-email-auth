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

    user = serializer.save()

    assert user.username == data['username']
    assert user.check_password(data['password'])
    assert user.email_addresses.count() == 1

    email = user.email_addresses.get()

    assert email.email == data['email']
