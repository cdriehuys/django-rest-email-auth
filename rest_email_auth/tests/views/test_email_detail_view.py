from rest_framework import status
from rest_framework.reverse import reverse

from rest_email_auth import serializers


def test_delete(api_client, email_factory):
    """
    Sending a DELETE request to the view should delete the email address
    with the provided ID.
    """
    email = email_factory()
    user = email.user

    api_client.force_authenticate(user=user)

    url = reverse("rest-email-auth:email-detail", kwargs={"pk": email.pk})
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert user.email_addresses.count() == 0


def test_get(api_client, email_factory):
    """
    Sending a GET request to the view with the ID of an email address
    owned by the requesting user should return the given email address'
    information.
    """
    email = email_factory()
    api_client.force_authenticate(user=email.user)

    url = reverse("rest-email-auth:email-detail", kwargs={"pk": email.pk})
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK

    serializer = serializers.EmailSerializer(email)

    assert response.data == serializer.data


def test_get_anonymous(api_client):
    """
    Sending a GET request to the view as an anonymous user should return
    a permissions error.
    """
    url = reverse("rest-email-auth:email-detail", kwargs={"pk": 1})
    response = api_client.get(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_get_other_user_email(api_client, email_factory, user_factory):
    """
    Sending a GET request to the view with the ID of an email owned by
    a different user should return a 404 response.
    """
    email = email_factory()
    api_client.force_authenticate(user=user_factory())

    url = reverse("rest-email-auth:email-detail", kwargs={"pk": email.pk})
    response = api_client.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update(api_client, email_factory):
    """
    Sending a PATCH request to the view should allow for updating the
    email address associated with the endpoint.
    """
    email = email_factory(is_primary=False, is_verified=True)
    data = {"is_primary": True}

    api_client.force_authenticate(user=email.user)

    url = reverse("rest-email-auth:email-detail", kwargs={"pk": email.pk})
    response = api_client.patch(url, data)

    assert response.status_code == status.HTTP_200_OK

    email.refresh_from_db()
    serializer = serializers.EmailSerializer(email)

    assert response.data == serializer.data
