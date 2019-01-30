from rest_framework import status
from rest_framework.reverse import reverse

from rest_email_auth import serializers


url = reverse("rest-email-auth:email-list")


def test_create_email(api_client, user_factory):
    """
    Sending a POST request with valid data to the view should create a
    new email address associated with the account.
    """
    user = user_factory()
    api_client.force_authenticate(user=user)

    data = {"email": "test-add@example.com"}

    response = api_client.post(url, data)

    assert response.status_code == status.HTTP_201_CREATED

    serializer = serializers.EmailSerializer(user.email_addresses.get())

    assert response.data == serializer.data


def test_list_emails(api_client, email_factory, user_factory):
    """
    Sending a GET request to the view should return the requesting
    user's emails.
    """
    user = user_factory()
    email_factory(user=user)
    email_factory(user=user)

    # Create email address for other user
    email_factory()

    serializer = serializers.EmailSerializer(
        user.email_addresses.all(), many=True
    )

    api_client.force_authenticate(user=user)

    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == serializer.data


def test_list_emails_anonymous(api_client):
    """
    Sending a GET request to the view as an anonymous user should result
    in a permissions error.
    """
    response = api_client.get(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN
