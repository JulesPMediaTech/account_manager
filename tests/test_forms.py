# tests/test_forms.py
def test_login_form_requires_username(app):
    with app.test_request_context():
        from app.forms import LoginForm
        form = LoginForm(data={'username': '', 'password': 'abc'})
        assert not form.validate()
        assert 'username' in form.errors

def test_login_form_requires_password(app):
    with app.test_request_context():
        from app.forms import LoginForm
        form = LoginForm(data={'username': 'user', 'password': ''})
        assert not form.validate()
        assert 'password' in form.errors

def test_user_form_email_blank_string_normalized(app):
    with app.test_request_context():
        from app.forms import UserForm
        from werkzeug.datastructures import MultiDict
        form = UserForm(MultiDict({'email': '   '}))
        form.process(MultiDict({'email': '   '}))
        assert form.email.data is None
