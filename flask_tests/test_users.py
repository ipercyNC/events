import json
from users.models import User

def test_register_user(client):     
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    login_data = {
        "username": "doesnt_exist",
        "password": "doesnt_exist"
    }
    register_response = client.post('/users/register', data=json.dumps(login_data), headers=headers)
    assert register_response.status_code == 200
    print(register_response.json['data']['username'])
    assert register_response.json['data']['username'] == 'doesnt_exist'


def test_login_user(client):     
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    # This user is created in the db setup for production and development
    login_data = {
        "username": "guest",
        "password": "test"
    }
    login_response = client.post('/users/login', data=json.dumps(login_data), headers=headers)
    assert login_response.status_code == 200

def test_get_user_by_id(app, client):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    # This user is created in the db setup for production and development
    login_data = {
        "username": "guest",
        "password": "test"
    }
    login_response = client.post('/users/login', data=json.dumps(login_data), headers=headers)
    assert login_response.status_code == 200
    with app.app_context():
        match = User.query.filter_by(username="guest").first()
        assert match != None
        get_user_by_id_response = client.get('/users/' + str(match.id), headers=headers)
        assert get_user_by_id_response.status_code == 200
        assert get_user_by_id_response.json['data']['username'] == 'guest'


def test_user_logout(client):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    # This user is created in the db setup for production and development
    login_data = {
        "username": "guest",
        "password": "test"
    }
    login_response = client.post('/users/login', data=json.dumps(login_data), headers=headers)
    assert login_response.status_code == 200

    logout_response = client.post('/users/logout', headers=headers)
    assert logout_response.status_code == 200
