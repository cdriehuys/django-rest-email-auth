.. _configuration-page:

=============
Configuration
=============

Some behaviors can be controlled by setting options in ``settings.py``. To
override a setting, add it to the ``REST_EMAIL_AUTH`` dictionary in the settings
file. For example::

    # settings.py

    REST_EMAIL_AUTH = {
        'EMAIL_VERIFICATION_URL': 'https://example.com/verify/{key}'
    }


Required Settings
=================

These settings must be configured before the app will function.

``EMAIL_VERIFICATION_URL``
--------------------------

A template for constructing the URL where a user can verify their email address.
This URL is sent to the user in the verification email after they add a new
email address. Any instance of ``{key}`` in the string will be replaced with the
key required to confirm that user's email.

``PASSWORD_RESET_URL``
----------------------

A template for constructing the URL where a user can reset their password. This
URL is sent to the user at the email address specified when the password reset
was requested. Any instance of ``{key}`` in the string will be replaced with the
key required to complete the password reset.


Additional Settings
===================

``CONFIRMATION_EXPIRATION``
---------------------------

Default: ``datetime.timedelta(days=1)``

The duration that an email confirmation key is valid for.


.. _confirmation-save-period:

``CONFIRMATION_SAVE_PERIOD``
----------------------------

Default: ``datetime.timedelta(days=7)``

The duration of the grace period after a confirmation expires before it will be
deleted by the ``cleanemailconfirmations`` command. See
:ref:`clean-email-confirmations` for more information.


``EMAIL_SUBJECT_DUPLICATE``
---------------------------

Default: ``Registration Attempt``

The subject line to use for emails notifying users of a registration attempt
for an email address that has already been registered.

``EMAIL_SUBJECT_VERFICATION``
-----------------------------

Default: ``Please Verify Your Email Address``

The subject line to use for emails containing a verification token for a
particular address.


.. _email-verification-password-required:

``EMAIL_VERIFICATION_PASSWORD_REQUIRED``
----------------------------------------

Default: ``True``

A boolean indicating if users must provide their password when verifying an
email address. Enabling this setting provides slightly more security at the
cost of a decreased user experience.

.. note::

    This setting was added in v2.0.0. To maintain backwards compatibility, it is enabled by default.


.. _config-registration-serializer:

``REGISTRATION_SERIALIZER``
---------------------------

Default: ``'rest_email_auth.serializers.RegistrationSerializer'``

The path to the serializer class that will be used for the registration
endpoint. See :ref:`custom-serializers-registration` for more information.

.. _config-path-to-reset-email-template:

``PATH_TO_RESET_EMAIL_TEMPLATE``
---------------------------

Default: ``rest_email_auth/emails/reset-password``

The path to the template for the reset password email.

.. _config-path-to-verify-email-template:

``PATH_TO_VERIFY_EMAIL_TEMPLATE``
---------------------------

Default: ``rest_email_auth/emails/verify-email``

The path to the template for the verify user email.

.. _config-path-to-duplicate-email-template:

``PATH_TO_DUPLICATE_EMAIL_TEMPLATE``
---------------------------

Default: ``rest_email_auth/emails/duplicate-email``

The path to the template for the email that notifies of a duplicate email.
