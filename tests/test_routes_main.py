import pytest


def test_root_redirects_to_index(client):
    response = client.get('/')
    assert response.status_code == 302
    assert '/index' in response.headers['Location']

def test_index_page_ok(client):
    response = client.get('/index')
    assert response.status_code == 200


@pytest.mark.parametrize(
    'role, expected_status',
    [
        (None, 403),
        ('user', 403),
        ('mod', 200),
        ('admin', 200),
        ('super', 200),
        ('viewer', 403),
        ('pro', 403),
        ('enterprise', 403),
    ],
)
def test_add_user_page_renders_by_role(client, mock_current_user, role, expected_status):
    mock_current_user(role=role)
    response = client.get('/add_user')
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'role, expected_status',
    [
        (None, 403),
        ('user', 403),
        ('mod', 200),
        ('admin', 200),
        ('super', 200),
        ('viewer', 403),
        ('pro', 403),
        ('enterprise', 403),
    ],
)
def test_show_user_table_ok_by_role(client, mock_current_user, role, expected_status):
    mock_current_user(role=role)
    response = client.get('/show_user_table')
    assert response.status_code == expected_status


def test_forward_user_id_valid_redirect(client, user_factory, mock_current_user):
    target_user = user_factory(role='user')
    mock_current_user(role='admin')
    response = client.post('/forward_user_id', data={
        'user_id': target_user.id,
        'redir': 'main.edit_user',
    })
    assert response.status_code == 302
    assert '/edit_user' in response.headers['Location']


def test_forward_user_id_invalid_redirect_falls_back(client, user_factory, mock_current_user):
    target_user = user_factory(role='user')
    mock_current_user(role='admin')
    response = client.post('/forward_user_id', data={
        'user_id': target_user.id,
        'redir': 'main.some_malicious_route',
    })
    assert response.status_code == 302
    assert '/show_user_table' in response.headers['Location']


def test_edit_user_without_user_id_redirects(client, mock_current_user):
    mock_current_user(role='mod')
    # No user set in userdb - should redirect away after passing auth.
    response = client.get('/edit_user')
    assert response.status_code == 302


def test_delete_user_nonexistent_redirects(client, mock_current_user):
    mock_current_user(role='admin')
    response = client.post('/delete_user', data={'user_id': '99999'})
    assert response.status_code == 302


@pytest.mark.parametrize(
    'role, expected_status',
    [
        (None, 403),
        ('user', 403),
        ('mod', 403),
        ('admin', 302),
        ('super', 302),
        ('viewer', 403),
        ('pro', 403),
        ('enterprise', 403),
    ],
)
def test_delete_user_access_control(client, mock_current_user, role, expected_status):
    mock_current_user(role=role)
    response = client.post('/delete_user', data={'user_id': '99999'})
    assert response.status_code == expected_status
