from app import create_app, init_db_and_jwt, setup_db
import json
from dotenv import load_dotenv
import os
load_dotenv()
def test_index_route():
        new_app = create_app()
        new_app.config.update({
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": os.getenv("TEST_DB_URL"),
            "SECRET_KEY": os.getenv("TEST_JWT_SECRET_KEY")
        })
        new_app = init_db_and_jwt(new_app)
        new_app = setup_db(new_app)
