# apps.reporting.routes
#https://www.loginradius.com/blog/engineering/guest-post/securing-flask-api-with-jwt/
from flask import Blueprint, current_app, request, abort, jsonify
from service.events import get_all_events
from service.users import get_all_users, get_user_by_username, get_password_hash, get_user_by_id, set_refresh_token
from flask_jwt_extended import create_refresh_token, create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from flask_jwt_extended import set_refresh_cookies, set_access_cookies
from flask_jwt_extended import decode_token
from functools import wraps
import jwt
from werkzeug.security import generate_password_hash, check_password_hash

auth_blueprint = Blueprint("auth_blueprint", __name__)

def token_required(fn):
    @wraps(fn)
    def decorated(*args, **kwargs):
        token = None
        if request.cookies.get('refresh_token_cookie', None):
            token = request.cookies.get('refresh_token_cookie')
        if not token:
            return {
                "message": "Refresh token missing",
                "error": "Unauthorized"
            }, 401
        try:
            current_user = jwt.decode(token, current_app.secret_key, algorithms=["HS256"])
            if current_user is None:
                return {
                "message": "Invalid token",
                "error": "Unauthorized"
            }, 401
        except jwt.ExpiredSignatureError as ex:
            return {
                "message": "Token expired",
                "error": str(e)
            }, 500
        except Exception as e:
            return {
                "message": "Error with token authentication",
                "error": str(e)
            }, 500

        return fn(current_user, *args, **kwargs)

    return decorated

@auth_blueprint.route("/users/login", methods=["POST"])
def login_user():
    data = request.json
    if not data:
        return {
            "message": "Please provide username and password",
            "error": "Bad Request"
        }, 400
    username = data.get("username", None)
    password = data.get("password", None)  
    if not username or not password:
        return {
            "message": "Please provide username and password",
            "error": "Bad Request"
        }, 400
    password_hash = get_password_hash(username)
    if not password_hash: 
        return {
            "message": "User does not exist, please register",
            "error": "Bad Request"
        }, 400
    if not check_password_hash(password_hash, password):
        return {
            "message": "Invalid password, please try again ",
            "error": "Bad Request"
        }, 400
    # generated_pass = generate_password_hash(password)
    refresh_token = create_refresh_token(identity=username)
    set_refresh_token(username, refresh_token)
    print(refresh_token)
    resp = jsonify( {
            "message": "Login success",
            "error": None
        })
    set_refresh_cookies(resp, refresh_token)
    return resp, 200

@auth_blueprint.route("/users/verify", methods=["GET"]) 
@token_required
def verify_user(current_user):
    return {
            "message": "All good here: " + current_user['sub'],
            "error": None
        }, 200

@auth_blueprint.route("/users", methods=["GET"])
@token_required
def view_users(current_user):
    return get_all_users()


@auth_blueprint.route("/users/<id>", methods=['GET'])
def get(id):
    return get_user_by_id(id)