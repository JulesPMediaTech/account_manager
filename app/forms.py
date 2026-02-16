from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp, InputRequired, EqualTo

class UserForm(FlaskForm):
    validatorsEnabled = False

    username = StringField('Username or email', validators=[
        InputRequired(message="Field cannot be empty"),
        Length(min=5, max=40, message="Must be between 5 and 40 characters")
    ] if validatorsEnabled else [])
    
    email = EmailField('Email', validators=[
        # InputRequired(message="Field cannot be empty"),
        Length(min=6, max=80, message="Must be between 6 and 80 characters")
    ] if validatorsEnabled else [])
    
    firstName = StringField('First Name', validators=[
        DataRequired(message="Field cannot be empty"), 
        Regexp(r'^[A-Za-z]+(?:[ -][A-Za-z]+)?$', message='Must contain letters or<br> spaced / hyphenated words')
    ] if validatorsEnabled else [])

    lastName = StringField('Last Name', validators=[
        DataRequired(message="Field cannot be empty"), 
        Regexp(r'^[A-Za-z]+(?:[ -][A-Za-z]+)?$', message='Must contain letters or<br> spaced / hyphenated words')
    ] if validatorsEnabled else [])
    
    role = SelectField('Role', choices=[
        ('super', 'Owner Super Admin'),
        ('admin', 'Administrator'),
        ('mod', 'Moderator'),
        ('enterprise', 'Enterprise User'),
        ('pro', 'Pro User'),
        ('user', 'User'),
        ('viewer', 'Viewer')
    ], default='user', validators=[DataRequired('must have a role assigned')])

    password = PasswordField('Password', validators=[
        InputRequired(message="Field cannot be empty"), 
        Length(min=7, max=20, message="Must be between 7 and 20 characters"),
        EqualTo('repeatPassword', message='Passwords must match')
    ] if validatorsEnabled else [],
                             render_kw={"autocomplete": "new-password"})

    repeatPassword = PasswordField('Repeat Password', validators=[
        InputRequired(message="Field cannot be empty")
    ] if validatorsEnabled else [],
                            render_kw={"autocomplete": "new-password"})

    submit = SubmitField('Submit')
    
    # cancel = SubmitField(name='Cancel', render_kw={'formnovalidate': True})
        
