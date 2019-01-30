import pytest

from rest_framework import status
from rest_framework.reverse import reverse

from rest_email_auth import serializers


url = reverse("rest-email-auth:resend-verification")


@pytest.mark.django_db
@pytest.mark.integration
def test_post_resend_verification(api_client):
    """
    Sending a POST request to the endpoint should send a confirmation
    email to the provided address.
    """
    data = {"email": "test@example.com"}

    response = api_client.post(url, data)

    assert response.status_code == status.HTTP_200_OK

    serializer = serializers.ResendVerificationSerializer(data=data)
    assert serializer.is_valid()

    assert response.data == serializer.data
