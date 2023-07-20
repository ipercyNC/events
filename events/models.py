# -*- coding: utf-8 -*-
"""
    users/events.py
    ~~~~~~~~~~~~~~

    Model class for the Event object (events table)
    Controls events that will be added by users to the DB/application

    2023 by Ian Percy
"""
from shared.db import db

# Event model object
class Event(db.Model):
    __tablename__ = "events"
    id = db.Column("id", db.Integer, primary_key=True)
    title = db.Column("title", db.String, unique=True, nullable=False)
    description = db.Column("description", db.String, nullable=False)
    user_id = db.Column("user_id", db.Integer, nullable=False)
    start_date = db.Column("start_date", db.DateTime)
    end_date = db.Column("end_date", db.DateTime)

    # Function to print out variables in JSON/object format 
    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "user_id": self.user_id, 
            "start_date": self.start_date,
            "end_date": self.end_date
        }