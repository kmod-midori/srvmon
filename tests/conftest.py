import os, sys
import tempfile
import pytest

from dotenv import load_dotenv
from flask_socketio.test_client import SocketIOTestClient


@pytest.fixture(scope='session')
def app():
    load_dotenv(
        dotenv_path=os.path.join(os.path.dirname(__file__), ".flaskenv"))

    db_fd, db_path = tempfile.mkstemp()
    os.environ['DATABASE_URI'] = f"sqlite:///{db_path}"

    from app import app, db
    from app.security import user_datastore
    with app.app_context():
        db.create_all()
        user_datastore.create_user(email="test@example.com",
                                   password="12345678")
        db.session.commit()
    yield app

    # close and remove the temporary database
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture(scope='session')
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture(scope='session')
def client_l(app):
    client = app.test_client()
    rv = client.post(
        '/api/accounts/login',
        data=dict(email="test@example.com", password="12345678"),
    )
    assert rv.status_code == 302
    return client


@pytest.fixture(scope='session')
def db(app):
    from app import db
    return db

@pytest.fixture(scope='session')
def socket_client(app, client_l):
    from app import socketio
    return SocketIOTestClient(app, socketio, flask_test_client=client_l)

@pytest.fixture(scope='session')
def mail(app):
    from app.mail import mail
    return mail
