# -*- coding: utf-8 -*-
"""
    users/models.py
    ~~~~~~~~~~~~~~

    Model class for the User object (users table)
    Controls users that will interact with the DB/application

    2023 by Ian Percy
"""
from shared.db import db


class User(db.Model):
    __tablename__ = "users"
    id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column("username", db.String, unique=True, nullable=False)
    password = db.Column("password", db.String, nullable=False)
    email = db.Column("email", db.String)
    refresh_token = db.Column("refresh_token", db.String)
    date_created = db.Column("date_created", db.Date, default=db.func.current_date())

    def to_json(self):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "email": self.email,
            "refresh_token": self.refresh_token,
            "date_created": self.date_created,
        }

    def to_frontend_json(self):
        return {"username": self.username, "email": self.email}
