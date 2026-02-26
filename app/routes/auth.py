from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from ..models import User
from ..forms import LoginForm
from werkzeug.security import check_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        print ('authenticated... going back to index')
        return redirect(url_for('main.index')), 302
    
    form = LoginForm()
    if form.validate_on_submit():
        print (f'got {form.data}')
        
        user = User.query.filter_by(username=form.username.data).first()
        if user and form.password.data and check_password_hash(user.password_hash, form.password.data):
            login_user(user, remember=form.remember_me.data)
            # Redirect to the page the user was trying to access, or to the index
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            print ('UNsuccessful')
            flash('Login Unsuccessful. Please check username and password', 'danger')
            return redirect(url_for('main.index'))
            
    return render_template('login.html', title='Sign In', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    print('Logging Out....')
    return redirect(url_for('main.index'))


