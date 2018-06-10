"""
Custom signals used by django-rest-email-auth.

These signals allow other applications to easily add custom behavior to
processes from this module.
"""

from django import dispatch


email_verified = dispatch.Signal(providing_args=['email'])

user_registered = dispatch.Signal(providing_args=['user'])
