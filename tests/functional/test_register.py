from flask import url_for

from awesomeapp.user.models import User
from awesomeapp.extensions import db

EMAIL_ALREADY_USED = 'Этот адрес электронной почты уже зарегистрирован'
SIGN_IN = 'Войти'
PASSWORDS_MUST_MATCH = 'Пароли должны совпадать'


def register(client, database, email, password, password2):
    """Запрос регистрации."""
    return client.post(url_for('user.register'), data={
        'email': email,
        'password': password,
        'password2': password2
        },
        follow_redirects=True
    )


def test_register(client, init_database):
    """Проверка успешной регистрации нового пользователя."""
    successful_registration = register(client, init_database,
                                       'new@user.com', '12345', '12345')
    is_user_exists = db.session.query(
        User.query.filter(User.email == 'new@user.com').exists()
        ).scalar()
    assert is_user_exists
    assert SIGN_IN in successful_registration.data.decode()


def test_register_different_passwords(client, init_database):
    """Проверка желаемого поведения регистрации в случае,
    если введены разные пароли."""
    different_passwords = register(client, init_database,
                                   'new@user.com', '12345', '123456')
    is_user_exists = db.session.query(
        User.query.filter(User.email == 'new@user.com').exists()
        ).scalar()
    assert not is_user_exists
    assert PASSWORDS_MUST_MATCH in different_passwords.data.decode()


def test_register_user_already_exists(client, database_with_user):
    """Проверка желаемого поведения регистрации в случае,
    если почта уже зарегистрирована."""
    user_already_exists = register(client, database_with_user,
                                   'test@test.test', '12345', '12345')
    assert EMAIL_ALREADY_USED in user_already_exists.data.decode()
