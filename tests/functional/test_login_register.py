from awesomeapp.user.models import User

def register(test_client, init_database, email, password, password2):
    return test_client.post('/users/register', data=dict(
        email=email,
        password=password,
        password2=password2
        ),
        follow_redirects=True
    )


def test_register(test_client, init_database):
    response = register(test_client, init_database,
                        'new@user.com', '12345', '12345')
    user = User.query.filter_by(email='new@user.com').count()
    assert user == 1
    assert 'Войти' in response.data.decode()


def test_bad_register(test_client, init_database):
    different_passwords = register(test_client, init_database,
                                   'new@user.com', '12345', '123456')
    user = User.query.filter_by(email='new@user.com').count()
    assert user == 0
    assert 'Пароли должны совпадать' in different_passwords.data.decode()

    user_already_exist = register(test_client, init_database,
                                  'test@test.test', '12345', '12345')
    assert 'Этот адрес электронной почты уже зарегистрирован'\
        in user_already_exist.data.decode()


def login(test_client, init_database, email, password):
    return test_client.post('/users/login', data=dict(
        email=email,
        password=password
        ),
        follow_redirects=True
    )


def test_login(test_client, init_database):
    response = login(test_client, init_database, 'test@test.test', '12345')
    assert 'Инвентарь' in response.data.decode()


def test_bad_login(test_client, init_database):
    response = login(test_client, init_database, 'test77@test.test', '12345')
    assert 'Не правильные почта или пароль, или то и то:)'\
        in response.data.decode()