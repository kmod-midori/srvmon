from app import app
from blinker import Namespace
import eventlet
from .db import db, Contact

signals = Namespace()
signal_new_notification = signals.signal('new-notification')


def deliver_contact(server, record, contact):
    app.logger.info(
        "Delivering notification for #%d to contact #%d (online=%s)",
        server.id, contact.id, record.online)


def notify_state_changed(server, record):
    users = []
    for user in server.users:
        users.append(user.id)
    contacts = Contact.query.filter(Contact.user_id.in_(users)).all()
    for contact in contacts:
        eventlet.spawn_n(deliver_contact, server, record, contact)
