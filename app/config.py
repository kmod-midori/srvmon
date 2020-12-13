"""
Global Flask Application Setting
See `.flaskenv` for default settings.
"""

import os
from app import app


class Config(object):
    # If not set fall back to production for safety
    FLASK_ENV = os.getenv('FLASK_ENV', 'production')
    # Set FLASK_SECRET on your production Environment
    SECRET_KEY = os.getenv('FLASK_SECRET', 'Secret')

    SECURITY_PASSWORD_SALT = os.getenv('PASSWORD_SALT', '146585145368132386173505678016728509634')
    SECURITY_FLASH_MESSAGES = False
    SECURITY_URL_PREFIX = '/api/accounts'
    SECURITY_REGISTERABLE = bool(int(os.getenv('REGISTERABLE', '0')))
    SECURITY_CHANGEABLE = True
    SECURITY_REDIRECT_BEHAVIOR = "spa"
    # enforce CSRF protection for session / browser - but allow token-based
    # API calls to go through
    SECURITY_CSRF_PROTECT_MECHANISMS = ["session", "basic"]
    SECURITY_CSRF_IGNORE_UNAUTH_ENDPOINTS = True
    # Send Cookie with csrf-token. This is the default for Axios and Angular.
    SECURITY_CSRF_COOKIE = {"key": "XSRF-TOKEN"}
    WTF_CSRF_CHECK_DEFAULT = False
    WTF_CSRF_TIME_LIMIT = None

    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    APP_DIR = os.path.dirname(__file__)
    ROOT_DIR = os.path.dirname(APP_DIR)  # Last level
    DIST_DIR = os.path.join(ROOT_DIR, 'dist')

    if not os.path.exists(DIST_DIR):
        raise Exception('DIST_DIR not found: {}'.format(DIST_DIR))


app.config.from_object('app.config.Config')