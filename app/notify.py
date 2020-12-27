from app import app
from blinker import Namespace
import eventlet

signals = Namespace()
signal_new_notification = signals.signal('new-notification')


def notify_state_changed(server, record):
    pass
