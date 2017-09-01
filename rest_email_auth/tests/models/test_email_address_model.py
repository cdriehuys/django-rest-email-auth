from rest_email_auth import models


def test_create(user_factory):
    """
    Test creating an email address.
    """
    email = models.EmailAddress.objects.create(
        email='test@example.com',
        user=user_factory())

    assert not email.is_verified
