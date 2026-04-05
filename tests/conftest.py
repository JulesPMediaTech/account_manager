import pytest
import uuid
from types import SimpleNamespace
from app import create_app
from app.extensions import db as _db
from app.models import User
from werkzeug.security import generate_password_hash

@pytest.fixture(scope='session')
def app(tmp_path_factory):
    db_dir = tmp_path_factory.mktemp('db')
    db_file = db_dir / 'test.sqlite3'
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': f'sqlite:///{db_file}',
        'WTF_CSRF_ENABLED': False,
        'SECRET_KEY': 'test-secret-key',
    })
    with app.app_context():
        _db.create_all()
        yield app
        _db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def db(app):
    yield _db
    _db.session.rollback()

TEST_PASSWORD = 'password123'


@pytest.fixture
def user_factory(db):
    created_ids = []

    def _create_user(role='user', username=None, email=None, password=TEST_PASSWORD):
        suffix = uuid.uuid4().hex[:10]
        user = User(
            username=username or f"testuser_{role}_{suffix}",
            email=email or f"test_{role}_{suffix}@example.com",
            first_name='Test',
            last_name='User',
            role=role,
            password_hash=generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()
        created_ids.append(user.id)
        return user

    yield _create_user

    db.session.rollback()
    for user_id in created_ids:
        persisted = db.session.get(User, user_id)
        if persisted is not None:
            db.session.delete(persisted)
    db.session.commit()

@pytest.fixture
def test_user(db):
    suffix = uuid.uuid4().hex[:10]
    user = User(
        username=f"testuser_{suffix}",
        email=f"test_{suffix}@example.com",
        first_name='Test',
        last_name='User',
        role='user',
        password_hash=generate_password_hash(TEST_PASSWORD)
    )
    db.session.add(user)
    db.session.commit()

    user_id = user.id  # store primitive before yield
    yield user
    db.session.rollback()
    persisted = db.session.get(User, user_id)
    if persisted is not None:
        db.session.delete(persisted)
        db.session.commit()


@pytest.fixture
def force_login(client):
    def _login(user):
        response = client.post(
            '/login',
            data={'username': user.username, 'password': TEST_PASSWORD},
            follow_redirects=False,
        )
        assert response.status_code == 302
        with client.session_transaction() as sess:
            assert sess.get('_user_id') == str(user.id)
        return response

    return _login


@pytest.fixture
def mock_current_user(monkeypatch):
    def _set(role=None, username='test-staffer'):
        user = SimpleNamespace(
            is_authenticated=role is not None,
            role=role,
            username=username,
        )
        monkeypatch.setattr('app.custom_decorators.current_user', user)
        monkeypatch.setattr('app.routes.main.current_user', user)
        return user

    return _set
