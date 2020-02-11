from flask import url_for

from awesomeapp.user.models import User
from awesomeapp.extensions import db

EMAIL_ALREADY_USED = 'Этот адрес электронной почты уже зарегистрирован'


def register(client, init_database, email, password, password2):
    return client.post(url_for('user.register'), data={
        'email': email,
        'password': password,
        'password2': password2
        },
        follow_redirects=True
    )


def test_register(client, init_database):
    """Проверка успешной регистрации нового пользователя"""
    response = register(client, init_database,
                        'new@user.com', '12345', '12345')
    user = db.session.query(
        User.query.filter(User.email == 'new@user.com').exists()
        ).scalar()
    assert user is True
    assert 'Войти' in response.data.decode()


def test_bad_register(client, init_database):
    """Проверка желаемого поведения регистрации в ситуациях:
        - введены разные пароли
        - почта уже зарегистрирована"""
    different_passwords = register(client, init_database,
                                   'new@user.com', '12345', '123456')
    user = db.session.query(
        User.query.filter(User.email == 'new@user.com').exists()
        ).scalar()
    assert user is False
    assert 'Пароли должны совпадать' in different_passwords.data.decode()

    user_already_exist = register(client, init_database,
                                  'test@test.test', '12345', '12345')
    assert EMAIL_ALREADY_USED in user_already_exist.data.decode()
