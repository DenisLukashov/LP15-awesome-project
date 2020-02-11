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


@pytest.fixture
def test_client():
    flask_app = create_app(TestConfig)
    testing_client = flask_app.test_client()
    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client

    ctx.pop()


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
def init_database_with_equipment():
    db.create_all()

    user = User(email='test@test.test')
    user.set_password('12345')
    db.session.add(user)
    db.session.commit()

    equipment = Equipment(
        name='Name',
        user_id=user.id,
        type_id=1
    )
    db.session.add(equipment)
    db.session.commit()

    yield db

    db.drop_all()
