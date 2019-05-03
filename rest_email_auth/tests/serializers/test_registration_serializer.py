try:
    from unittest import mock
except ImportError:
    import mock

from django.contrib.auth import get_user_model

import pytest

from rest_email_auth import serializers


@pytest.mark.django_db
def test_create_new_user(registration_listener):
    """
    Saving a serializer with valid data should create a new user.
    """
    data = {
        "email": "test@example.com",
        "password": "password",
        "username": "user",
    }

    serializer = serializers.RegistrationSerializer(data=data)
    assert serializer.is_valid()

    with mock.patch(
        "rest_email_auth.serializers.models.EmailAddress.send_confirmation",  # noqa
        autospec=True,
    ) as mock_send_confirmation:
        user = serializer.save()

    assert user.username == data["username"]
    assert user.check_password(data["password"])
    assert user.email_addresses.count() == 1

    email = user.email_addresses.get()

    assert email.email == data["email"]
    assert email.is_primary

    # Make sure we sent out an email confirmation
    assert mock_send_confirmation.call_count == 1

    # Make sure we sent a registration event
    assert registration_listener.call_count == 1


def test_register_duplicate_email(email_factory, registration_listener):
    """
    Attempting to register with an email that has already been verified
    should send an email to the owner of the email address notifying
    them of the registration attempt.
    """
    email = email_factory()

    data = {"email": email.email, "password": "password", "username": "user"}

    serializer = serializers.RegistrationSerializer(data=data)
    assert serializer.is_valid()

    with mock.patch(
        "rest_email_auth.serializers.models.EmailAddress.send_duplicate_notification",  # noqa
        autospec=True,
    ) as mock_send_duplicate_signup:
        serializer.save()

    assert get_user_model().objects.count() == 1
    assert mock_send_duplicate_signup.call_count == 1

    # We should not get a registration event for a duplicate email
    assert registration_listener.call_count == 0


def test_validate_email_lowercase_domain():
    """
    The registration serializer should not change an email address with
    a lowercase domain.
    """
    email = "Test@example.com"
    serializer = serializers.RegistrationSerializer()

    assert serializer.validate_email(email) == email


def test_validate_email_mixed_case_domain():
    """
    If the domain portion of the email is mixed case, it should be
    converted to lowercase.
    """
    email = "Test@ExaMple.com"
    expected = "Test@example.com"
    serializer = serializers.RegistrationSerializer()

    assert serializer.validate_email(email) == expected


@pytest.mark.django_db
def test_validate_password():
    """
    Validating the serializer's data should run the provided password
    through Django's default password validation system.
    """
    data = {
        "email": "test@example.com",
        "password": "password",
        "username": "user",
    }

    serializer = serializers.RegistrationSerializer(data=data)

    with mock.patch(
        "rest_email_auth.serializers.password_validation.validate_password",  # noqa
        autospec=True,
    ) as mock_validate:
        assert serializer.is_valid()

    assert mock_validate.call_count == 1
    assert set(mock_validate.call_args[0]) == {data["password"]}
