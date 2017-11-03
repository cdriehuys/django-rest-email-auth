============
Installation
============


Requirements
============

  * Python 2.7, 3.4, 3.5, or 3.6
  * Django 1.10 or above


Getting the Package
===================

The easiest way to install the package is with pip.

To get the most recent release::

    $ pip install django-rest-email-auth

To get the most recent development build::

    $ pip install git+https://github.com/cdriehuys/django-rest-email-auth.git@development#egg=django-rest-email-auth


Required Configuration
======================

In :file:`settings.py`, make sure the following settings are present::

    INSTALLED_APPS = [
        # At least these default Django apps must be installed:
        'django.contrib.auth',
        'django.contrib.contenttypes',

        # DRF must be listed for the browseable API to work
        'restframework',

        # Finally, the app itself
        'rest_email_auth',
    ]


    # The minimal settings dict required for the app
    REST_EMAIL_AUTH = {
        'EMAIL_VERIFICATION_URL': 'https://example.com/verify/{key}',
    }


Email Setup
-----------

In addition to the above settings, we also require that Django be configured to send emails. Please configure any of the ``EMAIL_*`` settings that apply to your setup. See Django's `email settings`_ for more information.


URLs
----

After the settings have been configured, include the app's URLs in :file:`urls.py`::

    from django.conf.urls import include, url


    urlpatterns = [
        url(r'account/', include('rest_email_auth.urls')),
    ]


Post-Installation
=================

After the app has been installed and configured, its migrations must be run::

    $ manage.py migrate


.. _`email settings`: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
