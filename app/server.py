from flask import Flask, render_template, request, redirect, url_for
from flask_wtf.csrf import CSRFProtect
from wtforms import Form, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp, InputRequired, EqualTo
from flask_wtf import FlaskForm
from os import getenv
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
load_dotenv()

# Load SECRET_KEY from Docker secret or .env fallback
secret_key = getenv('SECRET_KEY')
if not secret_key:
    secret_path = Path('/run/secrets/secret_key')
    if secret_path.exists():
        secret_key = secret_path.read_text().strip()


class UserForm(FlaskForm):
    # StringField(Label, List of Validators)
    username = StringField('Username or email', validators=[
        InputRequired(message="Field cannot be empty"),
        Length(min=5, max=40, message="Must be between 5 and 40 characters")
    ])
    firstName = StringField('First Name', validators=[
        DataRequired(message="Field cannot be empty"), 
        Regexp(r'^[A-Za-z]+(?:[ -][A-Za-z]+)?$', message='Must contain letters or<br> spaced / hyphenated words')
    ])
    lastName = StringField('Last Name', validators=[
        DataRequired(message="Field cannot be empty"), 
        Regexp(r'^[A-Za-z]+(?:[ -][A-Za-z]+)?$', message='Must contain letters or<br> spaced / hyphenated words')
    ])
    password = PasswordField('Password', validators=[
        InputRequired(message="Field cannot be empty"), 
        Length(min=7, max=20, message="Must be between 7 and 20 characters"),
        EqualTo('repeatPassword', message='Passwords must match')
       
    ])
    repeatPassword = PasswordField('Repeat Password', validators=[
        InputRequired(message="Field cannot be empty"),
              
    ])
    submit = SubmitField('Submit')
    
app = Flask(__name__)

'''
N.B. to create a secret key, run the following in python shell:
python -c "import secrets; print(secrets.token_hex(32))"
'''
app.config['SECRET_KEY'] = secret_key
csrf = CSRFProtect(app)


print ('Running Account Manager Server...')

@app.route('/')
def home():
    return redirect(url_for('index'))

@app.route('/index', methods=['GET', 'POST'])
def index():
    form = UserForm()
    if form.validate_on_submit():
        # Access data securely via form.field.data
        print (f'got the response: {form.data}')
    else: # Reset any fields that have errors
        if request.method == 'POST' and form.errors:
            print(f'validation errors: {form.errors}')
            for field_name in form.errors:
                getattr(form, field_name).data = ''
 
    
    status = request.args.get('status', '')
    return render_template('index.html', status=status, form=form)





# main form submission handling
@app.route('/submit', methods=['POST'])
def handle_data():
    # 2. Retrieve data securely
    username = request.form.get('user-id')
    print (f'username: {username}')
    
    if username:
        # Process data (e.g., save to DB)
        return f"Hello, {username}!"
    
    return "Invalid Data", 400


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8000,debug=True)
    
    # for production use, uncomment below and install waitress
    # from waitress import serve
    # serve(app, host='0.0.0.0',port=4080)