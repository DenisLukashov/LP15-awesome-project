from awesomeapp.user.models import User


def test_start_page_healthcheck(test_client, init_database):
    response = test_client.get('/', follow_redirects=True)
    assert response.status_code == 200


def test_equipmnet_page_healthcheck(test_client, init_database):
    response = test_client.get('/equipment', follow_redirects=True)
    assert response.status_code == 200


def test_login_page_healthcheck(test_client, init_database):
    response = test_client.get('/users/login')
    assert response.status_code == 200


def test_register(test_client, init_database):
    response = test_client.post('/users/register', data=dict(
        email='new@user.com',
        password='12345',
        password2='12345'),
        follow_redirects=True
    )
    user = User.query.filter_by(email='new@user.com').count()
    assert user == 1
    assert 'Войти' in response.data.decode()


def login(test_client, init_database, email, password):
    # for rule in test_client.application.url_map.iter_rules():
    #     print(rule)
    return test_client.post('/users/login', data=dict(
        email=email,
        password=password
    ), follow_redirects=True)


def test_login(test_client, init_database):
    re = login(test_client, init_database, 'test@test.test', '12345')
    # print(re.location)
    # print(re.data.decode())
    assert re.status_code == 200
    assert 'Инвентарь' in re.data.decode()
