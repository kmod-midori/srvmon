from app import app
import functools
from flask_socketio import SocketIO, disconnect, emit, send, join_room, leave_room
from flask_security import current_user
from .checkers import signal_new_record

socketio = SocketIO(
    app,
    path="/api/socket.io",
    cors_allowed_origins='*',
)


def authenticated_only(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            disconnect()
        else:
            return f(*args, **kwargs)

    return wrapped


@socketio.on('connect')
def connect_handler():
    if not current_user.is_authenticated:
        return False
    # Receive notification
    join_room(f"notify:{current_user.id}")


@socketio.on('start_mon')
@authenticated_only
def start_mon(params):
    room = f"mon:{params['id']}"
    join_room(room)


@socketio.on('stop_mon')
@authenticated_only
def stop_mon(params):
    room = f"mon:{params['id']}"
    leave_room(room)


def on_new_record(sender, record):
    room = f"mon:{record.server_id}"
    socketio.emit('new_record', record.to_dict(), to=room, broadcast=True)


signal_new_record.connect(on_new_record)