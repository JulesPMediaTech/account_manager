# tests/test_app.py
def test_create_app_returns_flask_app(app):
    from flask import Flask
    assert isinstance(app, Flask)

def test_testing_mode_is_on(app):
    assert app.config['TESTING'] is True

def test_secret_key_is_set(app):
    assert app.config.get('SECRET_KEY') not in (None, '', 'your-secret-key-here')

def test_csrf_extension_registered(app):
    assert 'csrf' in app.extensions

def test_blueprints_registered(app):
    assert 'main' in app.blueprints
    assert 'auth' in app.blueprints
