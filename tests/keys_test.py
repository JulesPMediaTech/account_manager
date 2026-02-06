# import sys
# from pathlib import Path

# sys.path.insert(0, str(Path(__file__).parent.parent))

from app.OLD_ORIG_server import app, csrf
from flask_wtf.csrf import CSRFProtect

def test_secret_key_loaded():
    """Test that SECRET_KEY is loaded from .env"""
    assert app.config['SECRET_KEY'] is not None
    assert len(app.config['SECRET_KEY']) > 0
    assert app.config['SECRET_KEY'] != 'your-secret-key-here'  # Not a placeholder

def test_csrf_protection_enabled():
    """Test that CSRF protection is initialized"""
    assert 'csrf' in app.extensions
    ext = app.extensions['csrf']
    assert isinstance(ext, CSRFProtect)
    assert ext is csrf

def test_secret_key_used_by_flask():
    """Test that Flask can generate session tokens with the SECRET_KEY"""
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess['test'] = 'value'
        # If this doesn't raise, SECRET_KEY is properly configured
        assert True

def test_csrf_token_generation():
    """Test that CSRF tokens can be generated"""
    with app.test_client() as client:
        response = client.get('/index')
        assert response.status_code == 200
        # The form should contain a CSRF token if protection is working
        assert b'csrf_token' in response.data