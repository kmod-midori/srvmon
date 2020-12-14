from app import app

from flask_security import Security, SQLAlchemyUserDatastore
from flask_wtf import CSRFProtect

from .db import db, User, Role

# Enable CSRF on all api endpoints.
CSRFProtect(app)

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)
