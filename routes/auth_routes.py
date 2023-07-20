# -*- coding: utf-8 -*-
"""
    routes/auth_routes.py
    ~~~~~~~~~~~~~~

    Controller class for the auth/user routes

    Handles logic for logging in user, verifying user, registering user
    With some help from # https://www.loginradius.com/blog/engineering/guest-post/securing-flask-api-with-jwt/

    2023 by Ian Percy
"""
from flask import Blueprint, current_app, request, jsonify
from service.users import (
    get_all_users,
    get_user_by_username,
    get_password_hash,
    get_user_by_id,
    set_refresh_token,
    create_user,
)
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import (
    set_refresh_cookies,
    unset_jwt_cookies,
)
from functools import wraps
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from root_logger import logger

# Create the blueprint to be used in the application
auth_blueprint = Blueprint("auth_blueprint", __name__)


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
        logger.info("Validating token")
        token = None
        if request.cookies.get("refresh_token_cookie", None):
            token = request.cookies.get("refresh_token_cookie")
        # Check if browser has a refresh token and return message if none exists
        if not token:
            return {"message": "Refresh token missing", "error": "Unauthorized"}, 401
        try:
            current_user = jwt.decode(
                token, current_app.secret_key, algorithms=["HS256"]
            )
            # If token does not decode, return error
            if current_user is None:
                return {"message": "Invalid token", "error": "Unauthorized"}, 401
        except jwt.ExpiredSignatureError as ex:
            return {"message": "Token expired", "error": str(e)}, 500
        except Exception as e:
            return {"message": "Error with token authentication", "error": str(e)}, 500

        return fn(current_user, *args, **kwargs)

    return decorated


@auth_blueprint.route("/users/login", methods=["POST"], endpoint="login")
def login_user():
    """User login route

    Logs user into the application with username + password

    Args:
        (in body)
        username (string): username for the user
        password (string): password for the user

    Returns:
        resp (Response): Response with user object"""
    data = request.json
    if not data:
        return {
            "message": "Please provide username and password",
            "error": "Bad Request",
        }, 400
    username = data.get("username", None)
    # This needs to be encrypted on the frontend to prevent MITM attacks
    password = data.get("password", None)
    logger.info("User login " + username)

    if not username or not password:
        return {
            "message": "Please provide username and password",
            "error": "Bad Request",
        }, 400
    password_hash = get_password_hash(username)
    if not password_hash:
        return {
            "message": "User does not exist, please register",
            "error": "Bad Request",
        }, 400
    if not check_password_hash(password_hash, password):
        return {
            "message": "Invalid password, please try again ",
            "error": "Bad Request",
        }, 400
    # generated_pass = generate_password_hash(password)

    # Create token and set token + cookie
    refresh_token = create_refresh_token(identity=username)
    set_refresh_token(username, refresh_token)
    current_user = get_user_by_username(username)
    if not current_user:
        resp = jsonify(
            {
                "message": "No user found for username",
                "data": None,
                "error": "NO_USER_FOUND",
            }
        )
    else:
        resp = jsonify(
            {
                "message": "User found",
                "data": current_user,
                "error": None,
            }
        )
    set_refresh_cookies(resp, refresh_token)
    return resp, 200


@auth_blueprint.route("/users/register", methods=["POST"], endpoint="register")
def login_user():
    """User register route

    Register user the application with username + password

    Args:
        (in body)
        username (string): username for the user
        password (string): password for the user

    Returns:
        resp (Response): Response with user object"""
    data = request.json
    if not data:
        return {
            "message": "Please provide username and password",
            "data": None,
            "error": "Bad Request",
        }, 400
    username = data.get("username", None)
    # This needs to be encrypted on the frontend to prevent MITM attacks
    password = data.get("password", None)
    if not username or not password:
        return {
            "message": "Please provide username and password",
            "data": None,
            "error": "Bad Request",
        }, 400
    # If password_hash has a value, the user already exists
    password_hash = get_password_hash(username)
    if not password_hash:
        generated_pass = generate_password_hash(password)
        create_user(username, generated_pass)
    else:
        return {
            "message": "User already exists, please login",
            "data": None,
            "error": "Bad Request",
        }, 400
    # Create token and set token + cookie
    refresh_token = create_refresh_token(identity=username)
    set_refresh_token(username, refresh_token)
    current_user = get_user_by_username(username)
    if not current_user:
        resp = jsonify(
            {
                "message": "No user found for username",
                "data": None,
                "error": "NO_USER_FOUND",
            }
        )
    else:
        resp = jsonify(
            {
                "message": "User registered",
                "data": current_user,
                "error": None,
            }
        )
    set_refresh_cookies(resp, refresh_token)
    return resp, 200


@auth_blueprint.route("/users/verify", methods=["GET"], endpoint="verify_user")
@token_required
def verify_user(current_user):
    """User verify route

    Verify that the user is connected to the application

    Args:
        current_user (User): User object of the currently authenicated user
    Returns:
        resp (Response): Response with if user is connected or not"""

    return {
        "message": "User verified: " + current_user["sub"],
        "data": None,
        "error": None,
    }, 200


@auth_blueprint.route("/users", methods=["GET"], endpoint="get_all_users")
@token_required
def view_users():
    """Get all users route

    Return all users for the application

    Args:
        None
    Returns:
        resp (Response): Response with the user objects"""
    result = get_all_users()
    if result:
        resp = jsonify(
            {
                "message": "Users found",
                "data": result,
                "error": None,
            }
        )
    else:
        resp = jsonify(
            {
                "message": "No users found",
                "data": None,
                "error": "NO_USERS_FOUND",
            }
        )
    return resp, 200


@auth_blueprint.route("/users/<id>", methods=["GET"], endpoint="get_user_by_id")
def get(id):
    """Get user by id route

    Get a user from the application by id

    Args:
        id (int): user id to search for in the db
    Returns:
        resp (Response): Response with the user object"""
    result = get_user_by_id(id)
    if result:
        resp = jsonify(
            {
                "message": "User found",
                "data": result,
                "error": None,
            }
        )
    else:
        resp = jsonify(
            {
                "message": "No user found for id",
                "data": None,
                "error": "NO_USER_FOUND",
            }
        )
    return resp, 200


@auth_blueprint.route("/users/logout", methods=["POST"], endpoint="logout")
def login_user():
    """Logout application route

    Reset user cookie and log out of application

    Args:
        None
    Returns:
        resp (Response): Response with the the result of the logout"""
    resp = jsonify({"message": "Logout success", "data": None, "error": None})
    unset_jwt_cookies(resp)
    return resp, 200
