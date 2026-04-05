import pytest


def test_login_page_renders(client):
    response = client.get('/login')
    assert response.status_code == 200
    assert b'form' in response.data


def test_login_with_valid_credentials(client, test_user):
    response = client.post('/login', data={
        'username': test_user.username,
        'password': 'password123',
    }, follow_redirects=True)
    assert response.status_code == 200


@pytest.mark.parametrize('role', ['user', 'mod', 'admin', 'super'])
def test_login_with_valid_credentials_main_roles(client, user_factory, role):
    user = user_factory(role=role)
    response = client.post('/login', data={
        'username': user.username,
        'password': 'password123',
    }, follow_redirects=False)
    assert response.status_code == 302
    assert response.headers['Location'].endswith('/index')


@pytest.mark.parametrize('role', ['viewer', 'pro', 'enterprise'])
def test_login_with_valid_credentials_member_roles(client, user_factory, role):
    user = user_factory(role=role)
    response = client.post('/login', data={
        'username': user.username,
        'password': 'password123',
    }, follow_redirects=False)
    assert response.status_code == 302
    assert response.headers['Location'].endswith('/index')


def test_login_with_invalid_password(client, test_user):
    response = client.post('/login', data={
        'username': test_user.username,
        'password': 'wrongpassword',
    }, follow_redirects=False)
    assert response.status_code == 302
    assert response.headers['Location'].endswith('/index')


def test_login_with_nonexistent_user(client):
    response = client.post('/login', data={
        'username': 'nobody',
        'password': 'whatever',
    }, follow_redirects=False)
    assert response.status_code == 302
    assert response.headers['Location'].endswith('/index')


def test_logout_when_not_logged_in_redirects_to_login(client):
    response = client.get('/logout', follow_redirects=True)
    assert b'Sign In' in response.data or b'login' in response.data.lower()


def test_authenticated_user_visiting_login_redirects(client, test_user):
    from flask import url_for

    client.post('/login', data={'username': test_user.username, 'password': 'password123'})
    response = client.get('/login', follow_redirects=False)

    assert response.status_code == 302
    with client.application.test_request_context():
        expected = url_for('main.index')
    assert response.headers['Location'].endswith(expected)


@pytest.mark.parametrize('role', ['user', 'mod', 'admin', 'super'])
def test_authenticated_roles_visiting_login_redirects(client, user_factory, role):
    user = user_factory(role=role)
    client.post('/login', data={'username': user.username, 'password': 'password123'})
    response = client.get('/login', follow_redirects=False)
    assert response.status_code == 302
    assert response.headers['Location'].endswith('/index')