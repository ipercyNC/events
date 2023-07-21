# -*- coding: utf-8 -*-
"""
    service/events.py
    ~~~~~~~~~~~~~~

    Class for interacting with the events repository

    All DB interactions are added here 

    2023 by Ian Percy
"""
from flask import jsonify
from events.models import Event
from users.models import User
from shared.db import db
from root_logger import logger
from sqlalchemy import exc

def get_all_events():
    """Get all events from DB

    Args:
        None

    Returns:
        events (list): List of event objects"""
    try:
        query_results = Event.query.all()
        events = [e.to_json() for e in query_results]
        return events
    except exc.SQLAlchemyError as e:
        logger.error("Error getting all events from DB " + str(e))
        return None

def delete_event_by_id(id):
    """Delete event from db

    Args:
        id (int): event id to delete

    Returns:
        result (boolean): success of delete"""
    try:
        Event.query.filter_by(id=id).delete()
        db.session.commit()
        return True
    except exc.SQLAlchemyError as e:
        logger.error("Error deleting event by id " + str(e))
        return False

def get_events_by_username(username):
    """Get all events by username

    Args:
        username (string): event id to delete

    Returns:
        result (list): list of events for the user """
    try:
        match = User.query.filter_by(username=username).first()
        if match:
            results = Event.query.filter_by(user_id=match.id).all()
            events = [e.to_json() for e in results]
            return events
        else:
            logger.info("No user matches username " + username)
            return None
    except exc.SQLAlchemyError as e:
        logger.error("Error searching for event by username and id " + str(e))
        return None
    
def create_event(title, description, user_id, start_date, end_date):
    """Create event

    Args:
        title (string): title of the event to create
        description (string): description of the event to create
        user_id (int): id of the user to add the event for
        start_date (string/Date): start datetime of the event
        end_date (string/Date): end datetime of the event

    Returns:
        result (boolean): success of the addition """
    try:
        db.session.add(Event(title=title, description=description, 
            user_id=user_id, start_date=start_date, end_date=end_date))
        db.session.commit()
        return True
    except exc.SQLAlchemyError as e:
        logger.error("Error creating event " + str(e))
        return False