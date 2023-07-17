from flask import render_template, jsonify
from users.models import User
from shared.db import db

def get_all_users():
    query_results = User.query.all()
    users = [u.to_json() for u in query_results]
    return jsonify(users)

def get_user_by_username(username):
    match = User.query.filter_by(username=username).first()
    print(match)
    return match

def get_user_by_id(id):
    match = User.query.filter_by(id=id).first()
    return match.to_json()

def get_password_hash(username):
    match = User.query.filter_by(username=username).first()
    if match:
        return match.password
    return None

def set_refresh_token(username, token):
    User.query.filter_by(username=username).update({"refresh_token" : token})
