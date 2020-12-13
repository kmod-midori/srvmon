import os
from flask import Flask, current_app, send_file

app = Flask(__name__, static_url_path='', static_folder='../dist')

from .config import Config
app.logger.info('>>> {}'.format(Config.FLASK_ENV))


@app.route('/')
def index_client():
    return app.send_static_file('index.html')
