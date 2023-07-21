# -*- coding: utf-8 -*-
"""
    flask_tests/test_user_models.py
    ~~~~~~~~~~~~~~

    Test the users models

    2023 by Ian Percy
"""
from users.models import User


def test_new_user():
    """
    Test creating a new User object
    """
    user = User(
        username="unit_test",
        password="pbkdf2:sha256:600000$lsgfCqtcIyQNokGI$109ad5c1a015842f2d3ad42645f6827c6c8a4a6ba02fe69324f4ffbfa2d9a745",
        refresh_token="",
        email="guest@example.com",
    )
    assert user.email == "guest@example.com"
    assert user.username == "unit_test"