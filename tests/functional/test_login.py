from flask import url_for

DESCRIBE_YOURS_EQUIPMENT = 'Не забудьте подробно описать Ваш инвентарь'


def login(test_client, init_database, email, password):
    return test_client.post(url_for('user.login'), data={
        'email': email,
        'password': password
        },
        follow_redirects=True
    )


def test_login_without_equipment(client, init_database):
    """Проверка перенаправления пользователя на нужную страницу,
        когда у него нет инвентаря"""
    response = login(client, init_database, 'test@test.test', '12345')
    assert 'Инвентарь' in response.data.decode()
    assert 'История связанная с инвентарем' in response.data.decode()
    assert DESCRIBE_YOURS_EQUIPMENT in response.data.decode()


def test_login_with_equipment(client, database_with_equipment):
    """Проверка перенаправления пользователя на нужную страницу,
        когда у него есть инвентарь"""
    response = login(client, database_with_equipment,
                     'test@test.test', '12345')
    assert 'Вывести статистику' in response.data.decode()
    assert 'Об инвентаре' in response.data.decode()
    assert 'Добавить статистику' in response.data.decode()


def test_bad_login(client, init_database):
    """Проверка желаемого поведения логина в ситуациях:
        - почты нет в базе данных
        - не верный пароль"""
    user_not_exists = login(client, init_database,
                            'wrong_email@example.com', '12345')
    assert 'Не правильные почта или пароль' in user_not_exists.data.decode()

    bad_password = login(client, init_database,
                         'test@test.test', 'wrong_password')
    assert 'Не правильные почта или пароль' in bad_password.data.decode()
