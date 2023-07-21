# Events (Flask Events)
Welcome! This application allows users to login/register and view/search/delete events that they have added. 
This uses React (production build or local run), Flask, and a PostgreSQL (local or the live production one on render.com).

The main objects for the DB are: users and events. Users contain the user information for the event tracking.
Events contain simple events with a title, description, user associated with the event, start datetime, and end datetime.

This is running on the web. Check it out!
https://eventsservice.onrender.com/
## How to Run:
* Clone repo `git clone https://github.com/ipercyNC/events.git .`
* In root dir, install packages - `pip install -r requirements.txt`
* Change the `template.env` file to be only `.env`
* In the `.env` file set your PostgreSQL SQLAchemy string (for your local PostgreSQL db) and also the secret key for the JWT
* If running local, uncomment the `# app = setup_db(app) # Comment out unless needing a fresh setup of the DB` calls in `app.py` so that the local DB can be initialized
* In the root directory - run `python app.py` - this will create the development flask server
* In another terminal window, change directory to the frontend directory - install packages `npm install` and then after `npm run start`
* Natigate to `http://localhost:3000/` in a browser to use the app
** Note - both need to be running at the same time for the frontend and the backend to communicate
** The api calls will still be available without the frontend - but requires JWT, so Postman is recommended if just using api 

## Functionality
(If running local - base url in front of the api calls is `localhost:5000`. Otherwise, use the Render app url as the base url. )
1) User can login or register
- On the UI - enter username or password and press login or register (if new user)
- API call - POST, `/users/login`  or `/users/register`,    body `{'username': <username>, 'password': <password>}`, headers = application/json
- This will return 200 with a valid request and set the refresh token in the browser
2) View events
- On the UI - events will show up automatically for the user. Choose either the *VIEW EVENT CALENDAR* button or the *VIEW EVENT LIST* button to view events
- API call - GET, `/events/<username>`, (replace the <username> with the current user), headers = application/json
- This will return 200 with a valid request and a list of events
3) Add event
- On the UI - click the *Add Event* once logged in
- API call - POST, `/events`, 
    ```
    body {
        "title": <title>,
        "description": <description>,
        "username": <username>,
        "startDate": <start date>, -> datetime object
        "endDate": <end date> -> datetime object
    }
    ```
    headers= application/json
    Example payload
    ```
    {
        "title": "test event",
        "description": "test description",
        "username": "guest",
        "startDate": "2023-07-11T04:00:00.000Z",
        "endDate": "2023-07-21T06:00:00.000Z"
    }
    ```
- This will return 200 with a valid addition and will show up in the events in the UI
4) Search events
- Only possible in the UI -> click *Search By Title or Description* after logging in
- This will filter all events in the application by the characters entered
5) Delete Event
- On the UI - when viewing an event, click on the trashcan icon (delete) and the event will be removed from the UI and DB
- API call - DELETE, `/events/<id>`, (replace the <id> with the id of the event to delete), headers = application/json
- This will return 200 with a valid request and a list of events


 ## Tests:
 To run tests:
 * Clone repo `git clone https://github.com/ipercyNC/events.git .`
 * In root dir, install packages - `pip install -r requirements.txt`
 * change the `template.env` file to be only `.env`
 * Populate the `TEST_DB_URL` and `TEST_JWT_SECRET_KEY` values in the .env file
 * Uncomment the `# app = setup_db(app) # Comment out unless needing a fresh setup of the DB` calls in `app.py` so that the local DB can be initialized
 * In the root folder, run `python -m pytest`


## Notes:
* Development was started just using the pyscopg driver to do manual queries, but the SQLAlchemy was chosen to speed up 
the development. The functionality provided is cleaner than the quick implementation I would have been able to complete
for SQL queries and validation.
* I set this up initially to be run locally, but I developed it to be deployed and run on render.com. The Postgres server (production and testing)
are both hosted on render.com. The web service runs via gunicorn and is hosted on their servers. The UI needs to be refined but having
the application hosted/functional was the goal.
* Each time the application runs, it can create a fresh copy of the DB and deletes all current data. This is just for testing purposes and should be disabled if not wanting data to disappear.

## Future fixes/functionality adds
* Add more complex events - with categories and groupings
* The date localization in Postgres is different than the one provided by the React component- making display wrong at times
* Add testing frontend
* Add more robust error handling backend
* Add more robust error handling frontend