from rest_email_auth import models


def test_create(user_factory):
    """
    Test creating an email address.
    """
    email = models.EmailAddress.objects.create(
        email='test@example.com',
        user=user_factory())

    assert not email.is_verified


def test_string_conversion(email_factory):
    """
    Converting an email address to a string should return the email
    address.
    """
    email = email_factory()

    assert str(email) == email.email
