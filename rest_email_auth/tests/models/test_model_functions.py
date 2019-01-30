try:
    from unittest import mock
except ImportError:
    import mock

from rest_email_auth import models


def test_generate_token():
    """
    The generate token method should use Django's provided method of
    getting a random string to create a random string.
    """
    with mock.patch(
        "rest_email_auth.models.get_random_string", autospec=True
    ) as mock_random:
        models.generate_token()

    assert mock_random.call_count == 1
    assert mock_random.call_args[1] == {"length": 64}
