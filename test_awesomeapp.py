import os
import tempfile
from urllib.parse import urlparse

import pytest


from awesomeapp import app
from config import Config
from awesomeapp.extensions import db


@pytest.fixture
def client():
    db_fd, Config.DATABASE = tempfile.mkstemp()
    Config.TESTING = True

    with app.test_client() as client:
        with app.app_context():
            db.init_app
        yield client

    os.close(db_fd)
    os.unlink(Config.DATABASE)


# def test_login(client):
#     r = client.post('/users/login')
#     print(r.status)


def test_start_page_healthcheck(client):
    rv = client.get('/')
    print(rv.location)
    assert rv.status_code == 302
