import pytest
from awesomeapp import create_app

from awesomeapp.user.models import User
from config import Config
from awesomeapp.extensions import db


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    WTF_CSRF_ENABLED = False


@pytest.fixture
def test_client():
    flask_app = create_app(TestConfig)

    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    testing_client = flask_app.test_client()

    # Establish an application context before running the tests.
    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client  # this is where the testing happens!

    ctx.pop()


@pytest.fixture()
def init_database():
    # Create the database and the database table
    db.create_all()

    # Insert user data
    user1 = User(email='test@test.test')
    user1.set_password('12345')
    db.session.add(user1)


    # Commit the changes for the users
    db.session.commit()

    yield db  # this is where the testing happens!

    db.drop_all()


# def test_login(test_client, init_database):
#     response = test_client.post('/users/login', data=dict(
#         email='test@test.test',
#         password='12345',
#         password2='12345'),
#         follow_redirects=True
#     )
#     print(response.data.decode())
#     # assert 'Инвентарь' in response.data.decode()