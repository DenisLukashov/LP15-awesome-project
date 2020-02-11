from flask import url_for

DESCRIBE_YOURS_EQUIPMENT = 'Не забудьте подробно описать Ваш инвентарь'
EQUIPMENT = 'Инвентарь'
EQUIPMENT_STORY = 'История связанная с инвентарем'
SHOW_STASTICS = 'Вывести статистику'
ABOUT_EQUIPMENT = 'Об инвентаре'
ADD_STATISTICS = 'Добавить статистику'
WRONG_PASSWORD_OR_EMAIL = 'Не правильные почта или пароль'


def login(test_client, init_database, email, password):
    """Запрос логина."""
    return test_client.post(url_for('user.login'), data={
        'email': email,
        'password': password
        },
        follow_redirects=True
    )


def test_login_without_equipment(client, init_database):
    """Проверка перенаправления пользователя на нужную страницу,
        когда у него нет инвентаря."""
    response = login(client, init_database, 'test@test.test', '12345')
    assert EQUIPMENT in response.data.decode()
    assert EQUIPMENT_STORY in response.data.decode()
    assert DESCRIBE_YOURS_EQUIPMENT in response.data.decode()


def test_login_with_equipment(client, database_with_equipment):
    """Проверка перенаправления пользователя на нужную страницу,
        когда у него есть инвентарь."""
    response = login(client, database_with_equipment,
                     'test@test.test', '12345')
    assert SHOW_STASTICS in response.data.decode()
    assert ABOUT_EQUIPMENT in response.data.decode()
    assert ADD_STATISTICS in response.data.decode()


def test_bad_login(client, init_database):
    """Проверка желаемого поведения логина в ситуациях:
        - почты нет в базе данных
        - не верный пароль."""
    user_not_exists = login(client, init_database,
                            'wrong_email@example.com', '12345')
    assert WRONG_PASSWORD_OR_EMAIL in user_not_exists.data.decode()

    bad_password = login(client, init_database,
                         'test@test.test', 'wrong_password')
    assert WRONG_PASSWORD_OR_EMAIL in bad_password.data.decode()
