import os
from flask import Flask, current_app, send_file

app = Flask(__name__, static_url_path='', static_folder='../dist')

from .config import Config
app.logger.info('FLASK_ENV = {}'.format(Config.FLASK_ENV))

from .cron import cron
from .db import db, migrate
from .security import security
from .mail import mail

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index_client():
    return app.send_static_file('index.html')
