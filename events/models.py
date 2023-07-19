from flask import render_template
from shared.db import db

class Event(db.Model):
    __tablename__ = "events"
    id = db.Column("id", db.Integer, primary_key=True)
    title = db.Column("title", db.String, unique=True, nullable=False)
    description = db.Column("description", db.String, nullable=False)
    user_id = db.Column("user_id", db.Integer, nullable=False)
    start = db.Column("start", db.DateTime)
    end = db.Column("end", db.DateTime)

    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "user_id": self.user_id, 
            "start": self.start,
            "end": self.end
        }