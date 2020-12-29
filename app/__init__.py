from flask import Flask, request, send_file
import eventlet, os, logging
eventlet.monkey_patch()

dist_base = os.path.join(os.path.dirname(__file__), '../dist')

app = Flask(__name__, static_url_path='/static', static_folder=dist_base + '/static')

from .config import Config
if not app.debug:
    app.logger.setLevel(logging.INFO)

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
    return send_file(dist_base + '/index.html')

