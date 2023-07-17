from flask import render_template, jsonify
from events.models import Event
from shared.db import db

def get_all_events():
    query_results = Event.query.all()
    events = [e.to_json() for e in query_results]
    return jsonify(events)