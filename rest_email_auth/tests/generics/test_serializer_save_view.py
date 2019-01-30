from rest_framework import serializers, status

from rest_email_auth import generics


class ExampleSerializer(serializers.Serializer):
    """
    Serializer for testing views.
    """

    foo = serializers.CharField()

    def save(self):
        """
        Mock save method.
        """
        pass


class ExampleView(generics.SerializerSaveView):
    """
    View that extends from the generic view we're testing.
    """

    serializer_class = ExampleSerializer


def test_post_invalid(api_rf):
    """
    Sending an invalid POST request to the view should return the
    serializer's errors.
    """
    request = api_rf.post("/", {})
    response = ExampleView.as_view()(request)

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    serializer = ExampleSerializer(data={})
    assert not serializer.is_valid()

    assert response.data == serializer.errors


def test_post_valid(api_rf):
    """
    Sending a valid POST request to the view should call the
    serializer's ``save`` method and return the serializer's data.
    """
    data = {"foo": "bar"}

    request = api_rf.post("/", data)
    response = ExampleView.as_view()(request)

    assert response.status_code == status.HTTP_200_OK

    serializer = ExampleSerializer(data=data)
    assert serializer.is_valid()

    assert response.data == serializer.data
