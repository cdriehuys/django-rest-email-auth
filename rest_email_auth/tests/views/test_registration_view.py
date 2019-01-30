try:
    from unittest import mock
except ImportError:
    import mock

import pytest

from rest_framework import status

from rest_email_auth import app_settings, views


registration_view = views.RegistrationView.as_view()


@mock.patch(
    "rest_email_auth.views.app_settings.__class__.REGISTRATION_SERIALIZER",
    new_callable=mock.PropertyMock,
)
def test_get_serializer_class(mock_registration_serializer):
    """
    The view should use the serializer defined in the app's settings.
    """
    view = views.RegistrationView()
    expected = mock_registration_serializer.return_value

    assert view.get_serializer_class() == expected


@pytest.mark.django_db
def test_register(api_rf):
    """
    Sending a POST request with valid data to the view should register a
    new user.
    """
    data = {
        "email": "test@example.com",
        "password": "password",
        "username": "user",
    }

    serializer = app_settings.REGISTRATION_SERIALIZER(data=data)
    assert serializer.is_valid()

    request = api_rf.post("/", data)
    response = registration_view(request)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data == serializer.data
