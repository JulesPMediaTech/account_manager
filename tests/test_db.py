# tests/test_db.py
import pytest
from app.db import UserDatabase
from werkzeug.security import check_password_hash

@pytest.fixture
def userdb():
    return UserDatabase()

def test_register_user_success(app, db, userdb):
    with app.app_context():
        result = userdb.register_user({
            'username': 'regtest', 'email': 'reg@test.com',
            'firstName': 'Reg', 'lastName': 'Test',
            'role': 'user', 'password': 'mypassword'
        })
    assert result['status'] == 'success'

def test_register_user_hashes_password(app, db, userdb):
    with app.app_context():
        result = userdb.register_user({
            'username': 'hashtest', 'firstName': 'H', 'lastName': 'T',
            'role': 'user', 'password': 'plaintext'
        })
        from app.models import User
        # user = User.query.get(result['user_id'])
        user = db.session.get(User, result['user_id']) # updated to v2 to clear legacy warning
        assert check_password_hash(user.password_hash, 'plaintext')

def test_register_user_empty_data_returns_nothing_added(app, db, userdb):
    with app.app_context():
        result = userdb.register_user({})
    assert result['status'] == 'nothing-added'

def test_get_all_users_returns_list(app, db, test_user, userdb):
    with app.app_context():
        users = userdb.get_all_users()
    assert isinstance(users, list)

def test_get_user_from_id_valid(app, db, test_user, userdb):
    with app.app_context():
        user = userdb.get_user_from_id(test_user.id)
    assert user.username == test_user.username

def test_get_user_from_id_invalid(app, db, userdb):
    with app.app_context():
        user = userdb.get_user_from_id(99999)
    assert user is None

def test_set_and_get_user_id(userdb):
    userdb.user_id = 42
    assert userdb.user_id == 42

def test_get_user_id_before_set_returns_none():
    fresh = UserDatabase()
    assert fresh.user_id is None

def test_update_user_changes_field(app, db, test_user, userdb):
    with app.app_context():
        result = userdb.update_user(
            {'username': 'testuser', 'firstName': 'Updated', 'lastName': 'User',
             'role': 'admin', 'email': 'test@example.com'},
            test_user.id
        )
    assert 'success' in result['status']

def test_update_password_success(app, db, test_user, userdb):
    with app.app_context():
        result = userdb.update_password({'password': 'newpassword99'}, test_user.id)
    assert 'success' in result['status']

def test_update_password_empty_returns_no_changes(app, db, test_user, userdb):
    with app.app_context():
        result = userdb.update_password({'password': ''}, test_user.id)
    assert result['status'] == 'no-changes'

def test_delete_user_success(app, db, test_user, userdb):
    with app.app_context():
        result = userdb.delete_user(test_user.id)
    assert 'success' in result['status']

def test_delete_user_nonexistent(app, db, userdb):
    with app.app_context():
        result = userdb.delete_user(99999)
    assert result['status'] == 'error'

def test_to_dict_converts_correctly(app, db, test_user, userdb):
    with app.app_context():
        users = userdb.get_all_users()
        d = userdb.to_dict(users)
    assert isinstance(d, list)
    assert 'username' in d[0]
