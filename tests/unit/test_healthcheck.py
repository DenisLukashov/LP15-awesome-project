def test_start_page_healthcheck(test_client, init_database):
    response = test_client.get('/', follow_redirects=True)
    assert response.status_code == 200


def test_equipmnet_page_healthcheck(test_client, init_database):
    response = test_client.get('/equipment', follow_redirects=True)
    assert response.status_code == 200


def test_login_page_healthcheck(test_client, init_database):
    response = test_client.get('/users/login')
    assert response.status_code == 200
