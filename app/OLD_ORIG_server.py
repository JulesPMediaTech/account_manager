from flask import Flask, render_template, request, redirect, url_for
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField, PasswordField, SubmitField
# from wtforms import Form
from wtforms.validators import DataRequired, Length, Regexp, InputRequired, EqualTo
from flask_wtf import FlaskForm
from os import getenv
from dotenv import load_dotenv
# from pathlib import Path

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# Load environment variables from .env file (local use only)
load_dotenv()

    
def readSecret(env_var, file_path):
    secret = getenv(env_var)
    if not secret:
        with open(file_path, 'r') as f:
            secret = f.read().strip()
    return secret

# Load SECRET_KEY / DB_PASSWORD from Docker secret or .env fallback
secret_key = readSecret("SECRET_KEY", "/run/secrets/secret_key")
db_password = readSecret("DB_PASSWORD", "/run/secrets/db_password")

# Database setup
DATABASE_URL = f"postgresql://accmanager:{db_password}@postgres:5432/accmanager_db"
engine = create_engine(DATABASE_URL)

# Test connection
try:
    with engine.connect() as conn:
        print("✅ Database connected successfully")
except Exception as e:
    print(f"❌ Database connection failed: {e}")

Base = declarative_base()
Session = sessionmaker(bind=engine)

# Define your models
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)

# Create tables
Base.metadata.create_all(engine)


class UserForm(FlaskForm):
    validatorsEnabled = False
    username = StringField('Username or email', validators=[
        InputRequired(message="Field cannot be empty"),
        Length(min=5, max=40, message="Must be between 5 and 40 characters")
    ] if validatorsEnabled else [])
    
    firstName = StringField('First Name', validators=[
        DataRequired(message="Field cannot be empty"), 
        Regexp(r'^[A-Za-z]+(?:[ -][A-Za-z]+)?$', message='Must contain letters or<br> spaced / hyphenated words')
    ] if validatorsEnabled else [])
    
    lastName = StringField('Last Name', validators=[
        DataRequired(message="Field cannot be empty"), 
        Regexp(r'^[A-Za-z]+(?:[ -][A-Za-z]+)?$', message='Must contain letters or<br> spaced / hyphenated words')
    ] if validatorsEnabled else [])
    
    password = PasswordField('Password', validators=[
        InputRequired(message="Field cannot be empty"), 
        Length(min=7, max=20, message="Must be between 7 and 20 characters"),
        EqualTo('repeatPassword', message='Passwords must match')
    ] if validatorsEnabled else [])
    
    repeatPassword = PasswordField('Repeat Password', validators=[
        InputRequired(message="Field cannot be empty")
    ] if validatorsEnabled else [])
    
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
    print ("test")
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
    debug_mode = getenv('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0',port=8000,debug=True)
    
    # for production use, uncomment below and install waitress
    # from waitress import serve
    # serve(app, host='0.0.0.0',port=4080)