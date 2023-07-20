# -*- coding: utf-8 -*-
"""
    shared/jwt.py
    ~~~~~~~~~~~~~~

    Class for the JWTManager object to be shared across the app

    2023 by Ian Percy
"""
from flask_jwt_extended import JWTManager

jwt = JWTManager()
