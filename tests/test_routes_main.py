# tests/test_routes_main.py
def test_root_redirects_to_index(client):
    response = client.get('/')
    assert response.status_code == 302
    assert '/index' in response.headers['Location']

def test_index_page_ok(client):
    response = client.get('/index')
    assert response.status_code == 200

def test_add_user_page_renders(client):
    response = client.get('/add_user')
    assert response.status_code == 200

def test_show_user_table_ok(client):
    response = client.get('/show_user_table')
    assert response.status_code == 200

def test_receive_user_id_valid_redirect(client, test_user):
    response = client.post('/receive_user_id', data={
        'user_id': test_user.id,
        'redir': 'main.edit_user'
    })
    assert response.status_code == 302
    assert '/edit_user' in response.headers['Location']

def test_receive_user_id_invalid_redirect_falls_back(client, test_user):
    response = client.post('/receive_user_id', data={
        'user_id': test_user.id,
        'redir': 'main.some_malicious_route'
    })
    assert '/show_user_table' in response.headers['Location']

def test_edit_user_without_user_id_redirects(client):
    # No user set in userdb - should redirect away
    response = client.get('/edit_user')
    assert response.status_code == 302

def test_delete_user_nonexistent_redirects(client):
    response = client.post('/delete_user', data={'user_id': '99999'})
    assert response.status_code == 302
