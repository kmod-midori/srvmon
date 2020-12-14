from app import app

from flask_mail import Mail, Message

from .celery import celery

mail = Mail(app)

@celery.task
def send_mail(**kwargs):
    # Use the Flask-Mail extension instance to send the incoming ``msg`` parameter
    # which is an instance of `flask_mail.Message`
    mail.send(Message(**kwargs))