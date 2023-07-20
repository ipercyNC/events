from app import create_app, init_db_and_jwt, setup_db # Flask instance of the API
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
        mimetype = 'application/json'
        headers = {
            'Content-Type': mimetype,
            'Accept': mimetype
        }
        login_data = {
            "username": "test_user",
            "password": "test_user"
        }
        register_response = new_app.test_client().post('/users/register', data=json.dumps(login_data), headers=headers)
        assert register_response.status_code == 200


        event1_data = {
                    "title":"test title3",
                    "description": "test description",
                    "username":"test_user",
                    "startDate":"2023-07-17 08:00:00",
                    "endDate":"2023-07-17 09:00:00",
        }
        add_event_response = new_app.test_client().post('/events', data=json.dumps(event1_data), headers=headers)
        assert add_event_response.status_code == 200
