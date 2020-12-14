from app import app

from flask_security import Security, SQLAlchemyUserDatastore
from flask_wtf import CSRFProtect

from .db import db, User, Role
from .mail import send_mail

# Enable CSRF on all api endpoints.
CSRFProtect(app)

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

@security.send_mail_task
def delay_flask_security_mail(msg):
    send_mail.delay(
        subject=msg.subject,
        sender=msg.sender,
        recipients=msg.recipients,
        body=msg.body,
        html=msg.html,
    )
