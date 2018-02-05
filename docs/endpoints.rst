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


Listing or Creating Email Addresses
===================================

All the email addresses associated with a user can be listed using the following endpoint. This endpoint can also be used to add a new email address to the user's account.

.. http:get:: /emails/

    List the email addresses associated with the requesting user.

    :>jsonarr int id: The ID that uniquely identifies the email address.
    :>jsonarr string created_at: A timestamp identifying when the email address was added by the user.
    :>jsonarr string email: The email's actual address.
    :>jsonarr boolean is_primary: A boolean indicating if the address is the user's primary address.
    :>jsonarr boolean is_verified: A boolean indicating if the email address has been verified.

.. http:post:: /emails/

    Add a new email address for the requesting user.

    :<json string email: The address of the email to add.

    :>json int id: The ID that uniquely identifies the email address.
    :>json string created_at: A timestamp identifying when the email address was added by the user.
    :>json string email: The email's actual address.
    :>json boolean is_primary: A boolean indicating if the address is the user's primary address.
    :>json boolean is_verified: A boolean indicating if the email address has been verified.


Viewing, Modifying, or Deleting a Specific Email Address
========================================================

.. http:get:: /emails/(int:id)/

    Retrieve information about a specific email address.

    :param int id: The unique ID of the email address to retrieve.

    :>json int id: The ID that uniquely identifies the email address.
    :>json string created_at: A timestamp identifying when the email address was added by the user.
    :>json string email: The email's actual address.
    :>json boolean is_primary: A boolean indicating if the address is the user's primary address.
    :>json boolean is_verified: A boolean indicating if the email address has been verified.

    :status 200: The email address was successfully retrieved.
    :status 404: There is no email address with the provided `id` accessible to the requesting user.

.. http:put:: /emails/(int:id)/

    Update a specific email address.

    :param int id: The unique ID of the email address to retrieve.

    :<json string email: The original email address. This field may not be changed.
    :<json boolean is_primary: A boolean indicating if this address should be the user's primary email. This may only be ``true`` for a verified email.

    :>json int id: The ID that uniquely identifies the email address.
    :>json string created_at: A timestamp identifying when the email address was added by the user.
    :>json string email: The email's actual address.
    :>json boolean is_primary: A boolean indicating if the address is the user's primary address.
    :>json boolean is_verified: A boolean indicating if the email address has been verified.

    :status 200: The email address was successfully updated.
    :status 404: There is no email address with the provided `id` accessible to the requesting user.


.. http:patch:: /emails/(int:id)/

    Partially update a specific email address.

    :param int id: The unique ID of the email address to retrieve.

    :<json string email: *(Optional)* The original email address. This field may not be changed.
    :<json boolean is_primary: *(Optional)* A boolean indicating if this address should be the user's primary email. This may only be ``true`` for a verified email.

    :>json int id: The ID that uniquely identifies the email address.
    :>json string created_at: A timestamp identifying when the email address was added by the user.
    :>json string email: The email's actual address.
    :>json boolean is_primary: A boolean indicating if the address is the user's primary address.
    :>json boolean is_verified: A boolean indicating if the email address has been verified.

    :status 200: The email address was successfully updated.
    :status 404: There is no email address with the provided `id` accessible to the requesting user.


.. http:delete:: /emails/(int:id)/

    Delete the email address with the specified `id`.

    :param int id: The unique ID of the email address to delete.

    :status 204: The email address was successfully deleted.
    :status 404: There is no email address with the provided `id` accessible to the requesting user.


Password Resets
===============

Users may request a password reset using any of their verified emails.

Request a Reset
---------------

Sending a request to this endpoint will email the user a link that they can use to reset their password.

.. http:post:: /request-password-reset/

    Request a new password reset.

    :<json string email: The email address to send the reset token to.

    :status 200: This status is always returned to avoid leaking information about which emails exist in the system.

Reseting a Password
-------------------

After the user receives an email address with a token they can use to reset their password, this endpoint should be used.

.. http:post:: /reset-password/

    Reset the user's password.

    :<json string key: The token that the user was emailed authorizing the reset.
    :<json string password: The user's new password.

    :status 200: The user's password was reset successfully.
    :status 400: Either the provided key does not exist or has expired, or the provided password is invalid.
