# tests/test_auth.py
def test_login_page_renders(client):
    response = client.get('/login')
    assert response.status_code == 200
    assert b'form' in response.data

def test_login_with_valid_credentials(client, test_user):
    response = client.post('/login', data={
        'username': 'testuser', 'password': 'password123'
    }, follow_redirects=True)
    assert response.status_code == 200

def test_login_with_invalid_password(client, test_user):
    response = client.post('/login', data={
        'username': 'testuser', 'password': 'wrongpassword'
    }, follow_redirects=True)
    assert b'Login Unsuccessful' in response.data

def test_login_with_nonexistent_user(client):
    response = client.post('/login', data={
        'username': 'nobody', 'password': 'whatever'
    }, follow_redirects=True)
    assert b'Login Unsuccessful' in response.data

def test_logout_when_not_logged_in_redirects_to_login(client):
    response = client.get('/logout', follow_redirects=True)
    assert b'Sign In' in response.data or b'login' in response.data.lower()

def test_authenticated_user_visiting_login_redirects(client, test_user):
    from flask import url_for
    client.post('/login', data={'username': test_user.username, 'password': 'password123'})
    response = client.get('/login', follow_redirects=False)
    
    assert response.status_code == 302
    with client.application.test_request_context():
        expected = url_for('main.index')  # change endpoint name if yours differs
    assert response.headers['Location'].endswith(expected)