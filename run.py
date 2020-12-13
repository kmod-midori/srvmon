from dotenv import load_dotenv
load_dotenv(dotenv_path="./.flaskenv")

from app import app
from app.socketio import socketio

socketio.run(app, port=5000)
# To Run:
# python run.py