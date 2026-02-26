import pytest
import uuid
from app import create_app
from app.extensions import db as _db
from app.models import User
from werkzeug.security import generate_password_hash

@pytest.fixture(scope='session')
def app():
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
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
