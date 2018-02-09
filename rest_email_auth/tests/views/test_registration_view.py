import pytest

from rest_framework import status

from rest_email_auth import app_settings, views


registration_view = views.RegistrationView.as_view()


@pytest.mark.django_db
def test_register(api_rf):
    """
    Sending a POST request with valid data to the view should register a
    new user.
    """
    data = {
        'email': 'test@example.com',
        'password': 'password',
        'username': 'user',
    }

    serializer = app_settings.REGISTRATION_SERIALIZER(data=data)
    assert serializer.is_valid()

    request = api_rf.post('/', data)
    response = registration_view(request)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data == serializer.data
