from flask import url_for
import pytest

endpoints = ('user.register', 'user.logout', 'user.login',
             'equipment.equipment', 'vizit.start_page')


@pytest.mark.parametrize('endpoint', endpoints)
def test_pages_healthcheck(client, init_database, endpoint):
    """ Проверка конечных точек на доступность."""
    response = client.get(url_for(endpoint), follow_redirects=True)
    assert response.status_code == 200
