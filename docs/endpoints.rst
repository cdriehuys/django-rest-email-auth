=========
Endpoints
=========

All endpoints here are relative to the path the app's URLs are included under.


Registering a New User
======================

Once a user has submitted the registration form successfully, they will receive an email to verify their email address.

Due to privacy concerns related to exposing email addresses, a registration request with an email that is already in use will not fail. Instead it will send an email to the previously registered address notifying them of the registration attempt.

.. http:post:: /register/

    :<json string <User.USERNAME_FIELD>: The user's username.
    :<json string email: The user's email address.
    :<json string password: The user's password.

    :>json string <User.USERNAME_FIELD>: The username the user was created with.
    :>json string email: The email address the verification email was sent to.

    :status 201: The request was successful and an email has been sent to the provded address.
    :status 400: An invalid request was made. Check the response data for details.


Resending a Verification Email
==============================

If a user lost the original verification email or it has expired, this endpoint can be used to send a new verification.

In order to avoid exposing email addresses, submitting an email to this endpoint that is not in the database will appear to be a successful request but is actually a no-op.

.. http:post:: /resend-verification/

    :<json string email: The address to resend a verification email to.

    :>json string email: The address the new verification email was sent to.

    :status 200: The request was succesful.
    :status 400: An invalid request was made. Check the response data for details.


Verify an Email Address
=======================

After a user receives a verification key, this endpoint is used to verify the
email address.

.. http:post:: /verify-email/

    :<json string key: The verification key the user received.
    :<json string password: The user's password.

    :>json string email: The email address that was verified.

    :status 200: The returned email was successfully verified.
    :status 400: An invalid request was made. Check the response data for details.
