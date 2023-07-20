# -*- coding: utf-8 -*-
"""
    app.py
    ~~~~~~~~~~~~~~

    Main application and entry point into the application. 
    The application allows users to view events they've created, add, and delete as well.

    Runs with PostgreSQL + Flask. SQLAlcehmy provides the ORM.

    2023 by Ian Percy
"""
import os
from flask import Flask, render_template
from shared.db import db
from shared.jwt import jwt
from routes.auth_routes import auth_blueprint
from routes.event_routes import event_blueprint
from dotenv import load_dotenv
from sqlalchemy import exc, text
from users.models import User
from events.models import Event
from root_logger import logger
import json

load_dotenv()
def create_app():

    # Create application and setup the static folders (created with React npm build)
    app = Flask(
        __name__,
        static_url_path="",
        static_folder="./frontend/build",
        template_folder="./frontend/build",
    )
    # Setup the URL for SQLAlchemy and the secret key needed for our JWT
    # If fails to load from .env (development), read from the environment variables (production)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DB_URL") or os.environ.get("DB_URL")
    app.config["SECRET_KEY"] = os.getenv("JWT_SECRET_KEY") or os.environ.get(
        "JWT_SECRET_KEY"
    )


    # Register the auth/user blueprint and the events blueprint
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(event_blueprint)

    @app.errorhandler(Exception)
    def handle_exception(e): 
        # Return error information
        response = e.get_response()
        response.data = json.dumps({
            "code": e.code,
            "name": e.name,
            "description": e.description,
        })
        response.content_type = "application/json"
        return response

    # Render the main route for the application - serves the static html from React
    @app.route("/")
    def hello():
        return render_template("index.html")
    return app

def init_db_and_jwt(app):
    jwt.init_app(app)
    db.init_app(app)
    return app

def setup_db(app):
    # Init the DB on each application rerun- not fully necessary but keeps the 
    # DB in a clean state 
    with app.app_context():
        try:
            # Drop all tables
            sql = text("DROP SCHEMA public CASCADE;CREATE SCHEMA public;")
            db.session.execute(sql)
            db.session.commit()

            # Create tables
            db.create_all()
            db.session.commit()

            # Create a user
            test_user = "guest"
            db.session.add(
                User(
                    username=test_user,
                    password="pbkdf2:sha256:600000$lsgfCqtcIyQNokGI$109ad5c1a015842f2d3ad42645f6827c6c8a4a6ba02fe69324f4ffbfa2d9a745",
                    refresh_token="",
                    email="guest@example.com",
                )
            )
            db.session.commit()

            # Create an event
            match = User.query.filter_by(username=test_user).first()
            db.session.add(
                Event(
                    title="test title",
                    description="test description",
                    user_id=match.id,
                    start_date="2023-07-17 08:00:00",
                    end_date="2023-07-17 09:00:00",
                )
            )
            db.session.commit()

            logger.info("Creation successful")
            return app
        except exc.IntegrityError as e:
            logger.error(e)
            db.session.rollback()

def run_gunicorn():
    app = create_app()
    app = init_db_and_jwt(app)
    # app = setup_db(app) # Comment out unless needing a fresh setup of the DB
    return app
    
if __name__ == "__main__":
    logger.info("Server starting")
    app = create_app()
    app = init_db_and_jwt(app)
    # app = setup_db(app) # Comment out unless needing a fresh setup of the DB
    app.run(debug=False)


