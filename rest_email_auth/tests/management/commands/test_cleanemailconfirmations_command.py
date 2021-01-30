import datetime
from io import StringIO

from django.core import management

import pytest

from rest_email_auth import models


def test_clean_expired(email_confirmation_factory, settings):
    """
    Calling the command should remove any email confirmations that are
    a specified time older than their expiration date.
    """
    settings.REST_EMAIL_AUTH = {
        "CONFIRMATION_EXPIRATION": datetime.timedelta(seconds=0),
        "CONFIRMATION_SAVE_PERIOD": datetime.timedelta(seconds=0),
    }

    email_confirmation_factory()

    out = StringIO()
    management.call_command("cleanemailconfirmations", stdout=out)

    assert models.EmailConfirmation.objects.count() == 0
    assert "Removed 1" in out.getvalue()


def test_clean_just_expired(email_confirmation_factory, settings):
    """
    Email confirmations that have just expired should not be removed.
    """
    settings.REST_EMAIL_AUTH = {
        "CONFIRMATION_EXPIRATION": datetime.timedelta(seconds=0)
    }

    email_confirmation_factory()

    management.call_command("cleanemailconfirmations")

    assert models.EmailConfirmation.objects.count() == 1


@pytest.mark.django_db
def test_clean_none():
    """
    If there are no expired email confirmations, a message should be
    displayed indicating that nothing happened.
    """
    out = StringIO()
    management.call_command("cleanemailconfirmations", stdout=out)

    assert "No email confirmations to remove" in out.getvalue()
