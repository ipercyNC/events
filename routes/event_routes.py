# -*- coding: utf-8 -*-
"""
    routes/event_routes.py
    ~~~~~~~~~~~~~~

    Controller class for the event routes

    Handles logic for getting all events, getting by username, deleting event, and adding event
    With some help from # https://www.loginradius.com/blog/engineering/guest-post/securing-flask-api-with-jwt/

    2023 by Ian Percy
"""
from flask import Blueprint, current_app, request, jsonify
from service.events import (
    get_all_events,
    delete_event_by_id,
    get_events_by_username,
    create_event,
)
from service.users import get_user_by_username
from functools import wraps
import jwt
from dateutil.parser import parse

# Create blueprint to be used in the application
event_blueprint = Blueprint("event_blueprint", __name__)


def token_required(fn):
    """Token required decorator

    Check that the request has an active JWT token
    TODO: refactor to move into its own class
    Args:
        None

    Returns:
        current_user (User): User that is authenticated with the application
    """

    @wraps(fn)
    def decorated(*args, **kwargs):
        token = None
        if request.cookies.get("refresh_token_cookie", None):
            token = request.cookies.get("refresh_token_cookie")
        # Check if browser has a refresh token and return message if none exists
        if not token:
            return {
                "message": "Refresh token missing",
                "data": None,
                "error": "Unauthorized",
            }, 401
        try:
            current_user = jwt.decode(
                token, current_app.secret_key, algorithms=["HS256"]
            )
            # If token does not decode, return error
            if current_user is None:
                return {
                    "message": "Invalid token",
                    "data": None,
                    "error": "Unauthorized",
                }, 401
        except jwt.ExpiredSignatureError as ex:
            return {"message": "Token expired", "data": None, "error": str(e)}, 500
        except Exception as e:
            return {
                "message": "Error with token authentication",
                "data": None,
                "error": str(e),
            }, 500

        return fn(current_user, *args, **kwargs)

    return decorated


@event_blueprint.route("/events", methods=["GET"], endpoint="get_all_events")
@token_required
def view_users():
    """Get all events

    Get all events (from all users) from the application

    Args:
        None

    Returns:
        resp (Response): Response with the event objects"""
    return get_all_events()


@event_blueprint.route(
    "/events/<username>", methods=["GET"], endpoint="get_events_by_username"
)
@token_required
def view_events(current_user, username):
    """View events for the chosen user

    Args:
        (in body)
        username (string): username for the user

    Returns:
        resp (Response): Response with event objects"""
    result = get_events_by_username(username)
    if result:
        resp = jsonify(
            {
                "message": "Events found",
                "data": result,
                "error": None,
            }
        )
    else:
        resp = jsonify(
            {
                "message": "No events found",
                "data": None,
                "error": "NO_EVENTS_FOUND",
            }
        )
    return resp, 200


@event_blueprint.route("/events/<id>", methods=["DELETE"], endpoint="delete_event")
def delete_by_id(id):
    """Delete event by id route

    Delete an event by a specific event id

    Args:
        (in body)
        id (int): id for the event to delete

    Returns:
        resp (Response): Response with user object"""
    if delete_event_by_id(id):
        resp = jsonify(
            {
                "message": "Event deleted",
                "data": None,
                "error": None,
            }
        )
    else:
        resp = jsonify(
            {
                "message": "Event not deleted",
                "data": None,
                "error": "EVENT_DELETE_ERROR",
            }
        )
    return resp, 200


@event_blueprint.route("/events", methods=["POST"], endpoint="add_event")
def add_event():
    """Add event route

    Add an event to the application

    Args:
        (in body)
        title (string): title of the event to create
        description (string): description of the event to create
        username (string): username of the user to add the event for
        start_date (string/Date): start datetime of the event
        end_date (string/Date): end datetime of the event

    Returns:
        resp (Response): Response with the result of the event addition"""
    data = request.json
    if not data:
        return {"message": "Please enter event data", "error": "Bad Request"}, 400
    # Check input values exist
    title = data.get("title", None)
    description = data.get("description", None)
    username = data.get("username", None)
    start_date = data.get("startDate", None)
    end_date = data.get("endDate", None)
    # Current the current user from the username (needed for id storage in the events table)
    current_user = get_user_by_username(username)
    if not title or not description or not username or not start_date or not end_date:
        resp = jsonify({
            "message": "Please provide all information for the event",
            "data": None,
            "error": "Bad Request",
        })
        return resp, 400
    
    # Validate dates
    if not valid_date(start_date):
        resp = jsonify({
            "message": "Please provide valid start date",
            "data": None,
            "error": "Bad Request",
        })
        return resp, 400
    if not valid_date(end_date):
        resp = jsonify({
            "message": "Please provide valid end date",
            "data": None,
            "error": "Bad Request",
        })
        return resp, 400
    
    # Validate lengths of title and description
    if len(title) > 254:
        resp = jsonify({
            "message": "Title is too long, please add a shorter title",
            "data": None,
            "error": "Bad Request",
        })
        return resp, 400
    
    if len(description) > 254:
        resp = jsonify({
            "message": "Description is too long, please add a shorter description",
            "data": None,
            "error": "Bad Request",
        })
        return resp, 400
    # Create event and return response
    event = create_event(title, description, current_user.id, start_date, end_date)
    if event:
        resp = jsonify({"message": "Event created", "data": event, "error": None})
    else:
        resp = jsonify({"message": "Event not created", "data": None, "error": None})
    return resp, 200

def valid_date(date):
    if date:
        try: 
            parse(date)
            return True
        except:
            pass
    return False