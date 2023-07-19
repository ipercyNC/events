from flask import render_template, jsonify
from events.models import Event
from users.models import User
from shared.db import db

def get_all_events():
    query_results = Event.query.all()
    events = [e.to_json() for e in query_results]
    return jsonify(events)

def delete_event_by_id(id):
    Event.query.filter_by(id=id).delete()
    db.session.commit()

def get_events_by_username(username):
    match = User.query.filter_by(username=username).first()
    if match:
        results = Event.query.filter_by(user_id=match.id).all()
        events = [e.to_json() for e in results]
        return jsonify(events)
    return None
    
def create_event(title, description, user_id, start, end):
    db.session.add(Event(title=title, description=description, 
        user_id=user_id, start=start, end=end))
    db.session.commit()
