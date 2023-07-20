# -*- coding: utf-8 -*-
"""
    shared/db.py
    ~~~~~~~~~~~~~~

    Class for the SQLAchemy object to be shared across the app

    2023 by Ian Percy
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
