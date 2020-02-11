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
    SERVER_NAME = "127.0.0.1:5555"


@pytest.fixture
def app():
    app = create_app(TestConfig)
    return app


@pytest.fixture()
def init_database():
    db.create_all()

    user = User(email='test@test.test')
    user.set_password('12345')
    db.session.add(user)
    db.session.commit()

    yield db

    db.drop_all()


@pytest.fixture()
def database_with_equipment(init_database):
    equipment = Equipment(
        name='Name',
        user_id=1,
        type_id=1
    )
    db.session.add(equipment)
    db.session.commit()
