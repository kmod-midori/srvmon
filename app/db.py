from app import app

import json, contextlib
from datetime import datetime

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
    contacts = db.relationship('Contact',
                               backref=db.backref('user', lazy=True),
                               lazy=True)

    def to_dict(self):
        return {'id': self.id, 'email': self.email}


server_alert_user = db.Table(
    "server_alert_user",
    db.Column('server_id',
              db.Integer,
              db.ForeignKey("server.id"),
              primary_key=True),
    db.Column('user_id',
              db.Integer,
              db.ForeignKey("user.id"),
              primary_key=True))


class Server(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.Text, nullable=False)
    mode = db.Column(db.Text, nullable=False)
    config = db.Column(db.Text, nullable=False)  # Stored as JSON
    enabled = db.Column(db.Boolean, nullable=False)

    users = db.relationship('User',
                            secondary=server_alert_user,
                            lazy=True,
                            backref=db.backref('servers', lazy=True))
    records = db.relationship('Record',
                              lazy='dynamic',
                              backref=db.backref('server', lazy=False))

    def set_config(self, config):
        self.config = json.dumps(config)

    def get_config(self):
        return json.loads(self.config)

    def to_dict(self):
        return {
            'id': self.id,
            'label': self.label,
            'mode': self.mode,
            'config': self.get_config(),
            'enabled': self.enabled,
        }

    def to_dict_ext(self):
        """
        To dict with extra information that comes with an overhead
        """
        d = self.to_dict()
        lr = self.last_record()
        if lr:
            d['lastRecord'] = lr.to_dict()
        else:
            d['lastRecord'] = None
        return d

    def last_record(self):
        return self.records.order_by(Record.time.desc()).first()

    def is_online(self):
        last_record = self.last_record()
        if last_record:
            return last_record.online
        else:
            return None

    def new_record(self):
        return Record(server_id=self.id,
                      time=datetime.now(),
                      online=False,
                      latency=None,
                      message=None)


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    type = db.Column(db.String(20), nullable=False)
    config = db.Column(db.Text, nullable=False)  # Stored as JSON
    enabled = db.Column(db.Boolean, nullable=False)

    def set_config(self, config):
        self.config = json.dumps(config)

    def get_config(self):
        return json.loads(self.config)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'type': self.type,
            'config': self.get_config(),
            'enabled': self.enabled
        }


class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    server_id = db.Column(db.Integer,
                          db.ForeignKey("server.id"),
                          nullable=False,
                          index=True)
    time = db.Column(db.DateTime, nullable=False, index=True)
    online = db.Column(db.Boolean, nullable=False)
    latency = db.Column(db.Integer, nullable=True)
    message = db.Column(db.Text, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'server_id': self.server_id,
            'time': int(self.time.timestamp() * 1000),
            'online': self.online,
            'latency': self.latency,
            'message': self.message,
        }

    def expired(self, interval):
        delta = datetime.now().timestamp() - self.time.timestamp()
        return delta > interval


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    server_id = db.Column(db.Integer,
                          db.ForeignKey("server.id"),
                          nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    message = db.Column(db.Text, nullable=True)


@contextlib.contextmanager
def transaction():
    try:
        yield
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise