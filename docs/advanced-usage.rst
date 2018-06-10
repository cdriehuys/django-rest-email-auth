==============
Advanced Usage
==============


Signals
=======

`Signals <django-signals_>`_ allow other applications to hook into rest-email-auth and add custom behaviors for events from the app.

The signals referenced below are importable from ``rest_email_auth.signals``.


Email Verification
------------------

**Signal Name:** ``email_verified``

**Signal Arguments:**

* **email:** The ``EmailAddress`` instance that was verfied.

This signal is triggered after an email address is verifed using an ``EmailConfirmation`` instance. Unless you have added custom logic allowing email addresses to be unverified, you can assume that the instance will be marked as verified after this point.


Registration
------------

**Signal Name:** ``user_registered``

**Signal Arguments:**

* **user:**
  The ``settings.AUTH_USER_MODEL`` instance that just registered.

This signal is triggered after a user has successfully registered. It will not be triggered if a user attempts to register with a duplicate email address.

.. note::

    This signal fires before the user has verified their email address.


.. _django-signals: https://docs.djangoproject.com/en/dev/topics/signals/
