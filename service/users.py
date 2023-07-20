# -*- coding: utf-8 -*-
"""
    service/users.py
    ~~~~~~~~~~~~~~

    Class for interacting with the users repository

    All DB interactions are added here 

    2023 by Ian Percy
"""
from flask import  jsonify
from users.models import User
from shared.db import db
from root_logger import logger
from sqlalchemy import exc

def get_all_users():
    """Get all users from DB

    Args:
        None

    Returns:
        users (list): List of user objects"""
    try:
        query_results = User.query.all()
        users = [u.to_frontend_json() for u in query_results]
        return users
    except exc.SQLAlchemyError as e:
        logger.error("Error getting all users from DB " + e)
        return None


def get_user_by_username(username):
    """Get user by username

    Args:
        username (string): username to search for in the DB

    Returns:
        result (user): user object match"""
    try:
        match = User.query.filter_by(username=username).first()
        return match.to_frontend_json()
    except exc.SQLAlchemyError as e:
        logger.error("Error getting user by username " + e)
        return None   

def get_user_by_id(id):
    """Get user by id

    Args:
        id (int): user id to search for in the DB

    Returns:
        result (user): user object match"""
    try:
        match = User.query.filter_by(id=id).first()
        return match.to_frontend_json()
    except exc.SQLAlchemyError as e:
        logger.error("Error getting user by id " + e)
        return None   

def get_password_hash(username):
    """Get password hash by username

    Args:
        username (string): username to search for in the DB

    Returns:
        result (string): user password"""
    try:
        match = User.query.filter_by(username=username).first()
        if match:
            return match.password
        return None
    except exc.SQLAlchemyError as e:
        logger.error("Error getting user password hash " + e)
        return None   

def set_refresh_token(username, token):
    """Set refresh token for user

    Args:
        username (string): username to add the token for in the DB
        token (string): refresh token to add into the DB

    Returns:
        result (boolean): success of edit"""
    try:
        User.query.filter_by(username=username).update({"refresh_token" : token})
        db.session.commit()
        return True
    except exc.SQLAlchemyError as e:
        logger.error("Error setting user token " + e)
        return False   


def create_user(username, generated_pass):
    """Create new user

    Args:
        username (string): username for the new user
        generated_pass (string): password for the new user

    Returns:
        result (boolean): success of addition"""
    try:
        db.session.add(User(username=username, 
            password=generated_pass,
            refresh_token='', email=''))
        db.session.commit()
        return True
    except exc.SQLAlchemyError as e:
        logger.error("Error creating user " + e)
        return False   
