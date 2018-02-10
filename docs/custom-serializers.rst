==================
Custom Serializers
==================

.. _custom-serializers-registration:

Registration Serializer
=======================

It is fairly common to create a custom user model for a Django project. To accomodate this, you can easily substitute in a custom registration serializer that includes your added fields using the :ref:`config-registration-serializer` setting.

To specify additional fields, simply subclass the provided registration serializer as follows::

    from rest_email_auth.serializers import RegistrationSerializer


    class MyRegistrationSerializer(RegistrationSerializer):

        class Meta:
            # You must include the 'email' field for the serializer to work.
            fields = (
                MyUserModel.USERNAME_FIELD,
                'password',
                'email',
                'other',
                'required',
                'fields',
            )
            model = MyUserModel


The provided registration serializer handles the conditional creation of the user and sending out a confirmation email. If you need more flexibility than is achievable by overriding the ``Meta`` class, you will have to dig in to the source code of the provided serializer. Feel free to create an issue if you have difficulties with this process.
