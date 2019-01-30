try:
    from unittest import mock
except ImportError:
    import mock

from rest_framework import status
from rest_framework.reverse import reverse


url = reverse("rest-email-auth:password-reset-request")


@mock.patch(
    "rest_email_auth.views.serializers.PasswordResetRequestSerializer.save",
    autospec=True,
)
def test_request_reset(mock_save, api_client, email_factory):
    """
    Sending a POST request with valid data to the view should create a
    new password reset request.
    """
    email = email_factory(is_verified=True)
    data = {"email": email.email}

    response = api_client.post(url, data)

    assert response.status_code == status.HTTP_200_OK
    assert mock_save.call_count == 1
