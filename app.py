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

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

load_dotenv()
app = Flask(__name__,
            static_url_path='', 
            static_folder='./frontend/build',
            template_folder='./frontend/build')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DB_URL")
app.config['SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")
jwt.init_app(app)
db.init_app(app)

app.register_blueprint(auth_blueprint)
app.register_blueprint(event_blueprint)


@app.route("/")
def hello():
    return render_template('index.html')


## If you need to init db
with app.app_context():

    try:

        sql = text("DROP SCHEMA public CASCADE;CREATE SCHEMA public;")
        db.session.execute(sql)
        db.session.commit()

        db.create_all()
        db.session.commit()

        test_user = "guest"
        db.session.add(User(username=test_user, 
        password='pbkdf2:sha256:600000$lsgfCqtcIyQNokGI$109ad5c1a015842f2d3ad42645f6827c6c8a4a6ba02fe69324f4ffbfa2d9a745',
        refresh_token='', email='guest@example.com'))
        db.session.commit()
        # sql = text("SELECT column_name, data_type FROM information_schema.columns WHERE table_schema = 'public' AND table_name = 'users';")
        # result = db.session.execute(sql)
        # for r in result:
        #     print(r)
        match = User.query.filter_by(username=test_user).first()
        db.session.add(Event(title="test title", description="test description", 
            user_id=match.id, start="2023-07-17 08:00:00", end="2023-07-17 09:00:00"))
        db.session.commit()

        print("Creation successful")
    except exc.IntegrityError as e:
        print(e)
        db.session.rollback()