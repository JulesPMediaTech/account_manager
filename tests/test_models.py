# tests/test_models.py
from app.models import User
from werkzeug.security import check_password_hash, generate_password_hash
import pytest


def test_user_creation(db):
    user = User(
        username='newuser', email='new@example.com',
        first_name='New', last_name='Person', role='user',
        password_hash=generate_password_hash('secret')
    )
    db.session.add(user)
    db.session.commit()
    assert user.id is not None

def test_password_is_hashed(test_user):
    assert test_user.password_hash != 'password123'
    assert check_password_hash(test_user.password_hash, 'password123')

def test_default_role_is_user(db):
    user = User(username='roletest', first_name='A', last_name='B',
                password_hash='x')
    db.session.add(user)
    db.session.flush()  # applies column defaults without a full commit
    assert user.role == 'user'
    db.session.rollback()


def test_unique_username_constraint(db, test_user):
    from sqlalchemy.exc import IntegrityError
    duplicate = User(
        username=test_user.username,   # use fixture value
        email=f"dup_{test_user.username}@example.com",
        first_name="X",
        last_name="Y",
        password_hash="x",
    )
    db.session.add(duplicate)
    with pytest.raises(IntegrityError):
        db.session.commit()
    db.session.rollback()  # critical: clear failed transaction



def test_unique_email_constraint(db, test_user):
    from sqlalchemy.exc import IntegrityError
    duplicate = User(username='other', email=test_user.email,
                     first_name='X', last_name='Y', password_hash='x')
    db.session.add(duplicate)
    with pytest.raises(IntegrityError):
        db.session.commit()
    db.session.rollback()
