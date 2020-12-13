from app import app

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_security.models import fsqla_v2 as fsqla

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# User models
fsqla.FsModels.set_db_info(db)


class Role(db.Model, fsqla.FsRoleMixin):
    pass


class User(db.Model, fsqla.FsUserMixin):
    pass