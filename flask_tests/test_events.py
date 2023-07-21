# -*- coding: utf-8 -*-
"""
    flask_tests/test_events.py
    ~~~~~~~~~~~~~~

    Test the events endpoints

    2023 by Ian Percy
"""
import json
from service.events import get_events_by_username

def test_create_event(client):   
    """
    Test creating a new event
    """  
    # Login user for the JWT token
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    login_data = {
        "username": "guest",
        "password": "test"
    }
    login_response = client.post('/users/login', data=json.dumps(login_data), headers=headers)
    assert login_response.status_code == 200

    event1_data = {
                "title":"test title3",
                "description": "test description",
                "username":"guest",
                "startDate":"2023-07-17 08:00:00",
                "endDate":"2023-07-17 09:00:00",
    }
    add_event_response = client.post('/events', data=json.dumps(event1_data), headers=headers)
    assert add_event_response.status_code == 200

def test_create_and_get_events(client):
    """
    Test creating an event then gathering events for user
    """
    # Login the user for the JWT token
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    login_data = {
        "username": "guest",
        "password": "test"
    }
    login_response = client.post('/users/login', data=json.dumps(login_data), headers=headers)
    assert login_response.status_code == 200

    event1_data = {
                "title":"test title3",
                "description": "test description",
                "username":"guest",
                "startDate":"2023-07-17 08:00:00",
                "endDate":"2023-07-17 09:00:00",
    }
    add_event_response = client.post('/events', data=json.dumps(event1_data), headers=headers)
    assert add_event_response.status_code == 200

    # Get all events
    get_events_response = client.get("/events/guest", headers=headers)
    assert get_events_response.status_code == 200


def test_delete_event(app, client):
    """
    Test deleting an event
    """
    # Login the user for the JWT token
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    login_data = {
        "username": "guest",
        "password": "test"
    }
    login_response = client.post('/users/login', data=json.dumps(login_data), headers=headers)
    assert login_response.status_code == 200

    event1_data = {
                "title":"test title3",
                "description": "test description",
                "username":"guest",
                "startDate":"2023-07-17 08:00:00",
                "endDate":"2023-07-17 09:00:00",
    }
    add_event_response = client.post('/events', data=json.dumps(event1_data), headers=headers)
    assert add_event_response.status_code == 200
    with app.app_context():
        events = get_events_by_username("guest")
        first_event = events[0]

        # Delete user
        delete_event_response = client.delete("/events/" + str(first_event["id"]), headers=headers)    
        assert delete_event_response.status_code == 200
