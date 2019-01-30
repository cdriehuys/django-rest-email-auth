from rest_framework import status

from rest_email_auth import serializers, views


email_verification_view = views.EmailVerificationView.as_view()


def test_verify_email(
    api_rf, email_confirmation_factory, email_factory, user_factory
):
    """
    Sending a POST request with valid data to the endpoint should mark
    the associated email address as verified.
    """
    user = user_factory(password="password")
    email = email_factory(user=user)
    confirmation = email_confirmation_factory(email=email)

    data = {"key": confirmation.key, "password": "password"}

    serializer = serializers.EmailVerificationSerializer(data=data)
    assert serializer.is_valid()

    request = api_rf.post("/", data)
    response = email_verification_view(request)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == serializer.data
