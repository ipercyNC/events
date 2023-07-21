# -*- coding: utf-8 -*-
"""
    flask_tests/test_event_modules.py
    ~~~~~~~~~~~~~~

    Test the events models

    2023 by Ian Percy
"""
from events.models import Event


def test_new_event():
    """
    Test creating a new event object 
    """
    event = Event(
        title="test title 2",
        description="test description 2",
        user_id="1",
        start_date="2023-07-17 08:00:00",
        end_date="2023-07-17 09:00:00",
    )
    assert event.title == "test title 2"
    assert event.description == "test description 2"
