from app import app
import functools
from flask_socketio import SocketIO, disconnect, emit
from flask_security import current_user

socketio = SocketIO(app)


def authenticated_only(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            disconnect()
        else:
            return f(*args, **kwargs)

    return wrapped