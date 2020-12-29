from flask import Flask, request, send_file
import eventlet, os
eventlet.monkey_patch()

dist_base = os.path.join(os.path.dirname(__file__), '../dist')

app = Flask(__name__, static_url_path='/static', static_folder=dist_base + '/static')

from .config import Config
app.logger.info('FLASK_ENV = {}'.format(Config.FLASK_ENV))

from . import cron
from .db import db, migrate
from .security import security
from .mail import mail
from .api import api_bp
from .socketio import socketio

app.register_blueprint(api_bp, url_prefix='/api')

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index_client(path):
    print(path)
    return send_file(dist_base + '/index.html')

