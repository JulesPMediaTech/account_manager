from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SelectField, SubmitField, BooleanField, HiddenField, DateField
from wtforms.validators import DataRequired, Length, Regexp, InputRequired, EqualTo
from .roles import Roles as roles

class UserForm(FlaskForm):
    validatorsEnabled = False

    username = StringField('Username', validators=[
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
    
    role = SelectField('Role', choices=roles.allUsers, default='user', validators=[DataRequired('must have a role assigned')])

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
    
    def process(self, formdata=None, obj=None, data=None, **kwargs):
        super().process(formdata=formdata, obj=obj, data=data, **kwargs)
        if self.email.data and not self.email.data.strip():
            self.email.data = None
            
class UserCreateForm(UserForm):
    dateOfBirth = DateField('Date of Birth',format='%d/%m/%Y')

            
class DeactivateUserForm(FlaskForm):
    role = SelectField('Role', choices=roles.allInactive, default='disabled', validators=[DataRequired('choose type')])
    reason = StringField('Reason', validators=[DataRequired(message='Field cannot be empty')])
    submit = SubmitField('Submit')
        
        
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')
    
class DialogConfirm(FlaskForm):
    message = HiddenField(default='This is the default dialog message')
    submit = SubmitField('OK')