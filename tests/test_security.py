# tests/test_security.py
def test_csrf_error_returns_400(app):
    """Re-enable CSRF and test that missing token gives 400."""
    app.config['WTF_CSRF_ENABLED'] = True
    client = app.test_client()
    response = client.post('/login', data={
        'username': 'user', 'password': 'password'
    })
    assert response.status_code == 400
    app.config['WTF_CSRF_ENABLED'] = False

def test_open_redirect_not_allowed_after_login(client, test_user):
    """next= param should not redirect to external URLs."""
    response = client.post(
        '/login?next=http://evil.com',
        data={'username': 'testuser', 'password': 'password123'},
        follow_redirects=False
    )
    location = response.headers.get('Location', '')
    assert 'evil.com' not in location
