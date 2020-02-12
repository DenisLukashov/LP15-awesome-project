from flask import url_for

DESCRIBE_YOURS_EQUIPMENT = 'Не забудьте подробно описать Ваш инвентарь'
EQUIPMENT = 'Инвентарь'
EQUIPMENT_STORY = 'История связанная с инвентарем'
SHOW_STASTICS = 'Вывести статистику'
ABOUT_EQUIPMENT = 'Об инвентаре'
ADD_STATISTICS = 'Добавить статистику'
WRONG_PASSWORD_OR_EMAIL = 'Не правильные почта или пароль'


def login(client, database, email, password, redirects=True):
    """Запрос логина."""
    return client.post(url_for('user.login'), data={
        'email': email,
        'password': password
        },
        follow_redirects=redirects
    )


def test_login_without_equipment(client, database_with_user):
    """Проверка нужной страницы если, у пользователя нет инвентаря."""
    equipment_page = login(client, database_with_user,
                           'test@test.test', '12345')
    assert equipment_page.status_code == 200
    assert EQUIPMENT in equipment_page.data.decode()
    assert EQUIPMENT_STORY in equipment_page.data.decode()
    assert DESCRIBE_YOURS_EQUIPMENT in equipment_page.data.decode()


def test_login_without_equipment_redirect(client, database_with_user):
    """Проверка перенаправления пользователя на нужную страницу в случае,
        если у него нет инвентаря."""
    login_page = login(client, database_with_user,
                       'test@test.test', '12345', redirects=False)

    assert login_page.status_code == 302
    assert login_page.location == 'http://localhost/users/login'

    redirect_to_login_page = client.get(login_page.location)
    assert redirect_to_login_page.status_code == 302
    assert redirect_to_login_page.location == 'http://localhost/'

    redirect_to_start_page = client.get(redirect_to_login_page.location)
    assert redirect_to_start_page.status_code == 302
    assert redirect_to_start_page.location == 'http://localhost/equipment'

    redirect_to_equipment_page = client.get(redirect_to_start_page.location)
    assert redirect_to_equipment_page.status_code == 200
    assert redirect_to_equipment_page.location is None


def test_login_with_equipment(client, database_with_equipment_and_user):
    """Проверка нужной страницы если, у пользователя есть инвентарь."""
    statistics_menu = login(client, database_with_equipment_and_user,
                            'test@test.test', '12345')
    statistics_menu.status_code == 200
    assert SHOW_STASTICS in statistics_menu.data.decode()
    assert ABOUT_EQUIPMENT in statistics_menu.data.decode()
    assert ADD_STATISTICS in statistics_menu.data.decode()


def test_login_with_equipment_redirect(client,
                                       database_with_equipment_and_user):
    """Проверка перенаправления пользователя на нужную страницу в случае,
    если у него есть инвентарь."""
    login_page = login(client, database_with_equipment_and_user,
                       'test@test.test', '12345', redirects=False)

    assert login_page.status_code == 302
    assert login_page.location == 'http://localhost/users/login'

    redirect_to_login_page = client.get(login_page.location)
    assert redirect_to_login_page.status_code == 302
    assert redirect_to_login_page.location == 'http://localhost/'

    redirect_to_start_page = client.get(redirect_to_login_page.location)
    assert redirect_to_start_page.status_code == 302
    assert redirect_to_start_page.location == 'http://localhost/stats/menu/1'

    redirect_to_menu_page = client.get(redirect_to_start_page.location)
    assert redirect_to_menu_page.status_code == 200
    assert redirect_to_menu_page.location is None


def test_login_wrong_email(client,  database_with_user):
    """Проверка желаемого поведения логина в случае,
    если введена не верная почта"""
    user_not_exists = login(client,  database_with_user,
                            'wrong_email@example.com', '12345')
    assert WRONG_PASSWORD_OR_EMAIL in user_not_exists.data.decode()


def test_login_wrong_password(client, database_with_user):
    """Проверка желаемого поведения логина в случае,
    если введен не верный пароль"""
    wrong_password = login(client, database_with_user,
                           'test@test.test', 'wrong_password')
    assert WRONG_PASSWORD_OR_EMAIL in wrong_password.data.decode()
