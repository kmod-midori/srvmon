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

    def last_record(self):
        return self.records.order_by(Record.time.desc()).first()

    def should_check(self):
        last_record = self.last_record()
        config = self.get_config()
        interval = config['interval']
        return last_record is None or last_record.expired(interval)

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


class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    server_id = db.Column(db.Integer,
                          db.ForeignKey("server.id"),
                          nullable=False)
    time = db.Column(db.DateTime, nullable=False)
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


@contextlib.contextmanager
def transaction():
    try:
        yield
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise