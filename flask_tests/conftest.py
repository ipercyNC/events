# -*- coding: utf-8 -*-
"""
    flask_tests/conftest.py
    ~~~~~~~~~~~~~~

    Setup the fixtures for the testing

    2023 by Ian Percy
"""
import pytest
from app import create_app, init_db_and_jwt, setup_db
from dotenv import load_dotenv
import os

load_dotenv()

@pytest.fixture()
def app():
    """
    Create the app fixture to be used
    """
    new_app = create_app()
    new_app.config.update(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": os.getenv("TEST_DB_URL"),
            "SECRET_KEY": os.getenv("TEST_JWT_SECRET_KEY"),
        }
    )
    new_app = init_db_and_jwt(new_app)
    new_app = setup_db(new_app)

    yield new_app


@pytest.fixture()
def client(app):
    """
    Create the client fixture to be used
    """
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
