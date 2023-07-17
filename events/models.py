from flask import render_template
from shared.db import db

class Event(db.Model):
    __tablename__ = "events"
    id = db.Column("id", db.Integer, primary_key=True)
    title = db.Column("title", db.String, unique=True, nullable=False)
    description = db.Column("description", db.String, nullable=False)
    event_date = db.Column("event_date", db.Date, nullable=False)
    state = db.Column("state", db.String)
    city = db.Column("city", db.String)
    user_id = db.Column("user_id", db.Integer, nullable=False)
    date_created = db.Column("date_created", db.Date, default=db.func.current_date())

    def to_json(self):
        return {
            "title": self.title,
            "description": self.description,
            "event_date" : self.event_date,
            "state": self.state,
            "city": self.city,
            "user_id": self.user_id, 
            "date_created": self.date_created
        }