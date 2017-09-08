"""Serializers for the ``rest_email_auth`` app.

The serializers handle the conversion of data between the JSON or form
data the API receives and native Python datatypes.
"""

from django.contrib.auth import get_user_model

from rest_framework import serializers

from rest_email_auth import models


UserModel = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for registering new users.
    """
    email = serializers.EmailField()

    class Meta(object):
        extra_kwargs = {
            'password': {
                'style': {'input_type': 'password'},
                'write_only': True,
            },
        }
        fields = (UserModel.USERNAME_FIELD, 'email', 'password')
        model = UserModel

    def create(self, validated_data):
        """
        Create a new user from the data passed to the serializer.

        Args:
            validated_data (dict):
                The data passed to the serializer after it has been
                validated.

        Returns:
            A new user created from the provided data.
        """
        email = validated_data.pop('email')
        user = UserModel.objects.create_user(**validated_data)

        # We set an ephemeral email property so that it is included in
        # the data returned by the serializer.
        user.email = email

        models.EmailAddress.objects.create(email=email, user=user)

        return user
