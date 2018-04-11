==============
Advanced Usage
==============


Signals
=======

`Signals <django-signals_>`_ allow other applications to hook into rest-email-auth and add custom behaviors for events from the app.

The signals referenced below are importable from ``rest_email_auth.signals``.


Registration
------------

**Signal Name:** ``user_registered``

This signal is triggered after a user has successfully registered. It will not be triggered if a user attempts to register with a duplicate email address.

.. note::

    This signal fires before the user has verified their email address.


.. _django-signals: https://docs.djangoproject.com/en/dev/topics/signals/
