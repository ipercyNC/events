from flask import Blueprint, current_app, request, abort, jsonify
from service.events import get_all_events
from service.users import get_all_users, get_user_by_username, get_password_hash, set_refresh_token
from flask_jwt_extended import create_refresh_token, create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from flask_jwt_extended import set_refresh_cookies, set_access_cookies
from flask_jwt_extended import decode_token
from functools import wraps
import jwt
from werkzeug.security import generate_password_hash, check_password_hash

event_blueprint = Blueprint("event_blueprint", __name__)

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
    
@event_blueprint.route("/events", methods=["GET"])
@token_required
def view_users(current_user):
    return get_all_events()