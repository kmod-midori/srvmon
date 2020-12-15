from app import app

from flask_security import Security, SQLAlchemyUserDatastore
from flask_wtf import CSRFProtect

from .db import db, User, Role
from .utils import render_json

# Enable CSRF on all api endpoints.
CSRFProtect(app)

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

@security.render_json
def sec_render_json(payload, code, headers=None, user=None):
    return render_json(payload, code, headers)