import pytest

from awesomeapp import create_app
from awesomeapp.user.models import User
from awesomeapp.equipment.models import Equipment
from config import Config
from awesomeapp.extensions import db


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    WTF_CSRF_ENABLED = False
    HOST = '127.0.0.1'
    PORT = '5555'
    SERVER_NAME = '127.0.0.1:5555'


@pytest.fixture
def app():
    flask_app = create_app(TestConfig)
    return flask_app


@pytest.fixture()
def init_database():
    db.create_all()

    yield db

    db.drop_all()


@pytest.fixture()
def database_with_user(init_database):
    user = User(email='test@test.test')
    user.set_password('12345')
    db.session.add(user)
    db.session.commit()


@pytest.fixture()
def database_with_equipment_and_user(init_database):
    user = User(email='test@test.test')
    user.set_password('12345')
    db.session.add(user)

    equipment = Equipment(
        name='Name',
        user_id=1,
        type_id=1
    )
    db.session.add(equipment)
    db.session.commit()
