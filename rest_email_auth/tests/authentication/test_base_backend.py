def test_get_user(base_auth_backend, user_factory):
    """
    Passing in a user's ID should return the user with that ID.
    """
    user = user_factory()

    assert base_auth_backend.get_user(user.id) == user


def test_get_user_invalid_id(base_auth_backend, db):
    """
    Passing in an ID with no corresponding user should return None.
    """
    assert base_auth_backend.get_user(1) is None
