from app import app
from blinker import Namespace
import eventlet, requests
from .db import db, Contact
from .mail import mail
from flask_mail import Message

signals = Namespace()
signal_new_notification = signals.signal('new-notification')


def deliver_email(server, record, contact):
    if record.online:
        status = 'ONLINE'
        message = None
    else:
        status = 'OFFLINE'
        message = record.message
    address = contact.get_config()['address']

    html = f"Server <b>{server.label}</b> is currently <b>{status}</b>"
    if message is not None:
        html += f": {message}"

    with app.app_context():
        msg = Message(f"{server.label} is {status}", recipients=[address])
        msg.html = html
        mail.send(msg)


def create_payload_discord(content):
    return dict(content=content)


def create_payload_ding(content):
    return dict(msgtype='text', text=dict(content=content))


payload_creator = {
    'discord': create_payload_discord,
    'ding': create_payload_ding
}


def deliver_webhook(server, record, contact):
    if record.online:
        status = 'ONLINE'
        message = None
    else:
        status = 'OFFLINE'
        message = record.message
    config = contact.get_config()
    url = config['url']
    service = config['service']

    content = f"Server {server.label} is currently {status}"
    if message is not None:
        content += f": {message}"

    payload = payload_creator[service](content)

    rv = requests.post(url,
                       json=payload,
                       timeout=app.config['WEBHOOK_TIMEOUT'] / 1000)
    rv.raise_for_status()


deliver_methods = dict(email=deliver_email, webhook=deliver_webhook)


def deliver_contact(server, record, contact):
    app.logger.info(
        "Delivering notification for #%d to contact #%d (online=%s)",
        server.id, contact.id, record.online)
    try:
        deliver_methods[contact.type](server, record, contact)
    except Exception as e:
        app.logger.error(
            "Failed to deliver notification for #%d to contact #%d: %s",
            server.id, contact.id, e)
    else:
        app.logger.info("Notification for #%d delivered to contact #%d.",
                        server.id, contact.id)


def notify_state_changed(server, record):
    users = []
    for user in server.users:
        users.append(user.id)
        signal_new_notification.send(server=server, user=user, record=record)
    contacts = Contact.query.filter(Contact.user_id.in_(users)).all()
    for contact in contacts:
        if contact.enabled:
            eventlet.spawn_n(deliver_contact, server, record, contact)
