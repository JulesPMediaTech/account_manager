from flask import Blueprint, render_template, request, redirect, url_for
from ..forms import UserForm
from ..db import userdb

bp = Blueprint('main', __name__)

@bp.route('/')
def home():
    return redirect(url_for('main.index'))

@bp.route('/index')
def index():
    status = request.args.get('status', '')
    return render_template('index.html', status=status, title="Account Manager")

@bp.route('/add_user', methods=['GET','POST'])
def add_user():
    form = UserForm()
    if form.validate_on_submit():
        print ('sending form data')
    else:
        if request.method == 'POST' and form.errors:
            print(f'validation errors: {form.errors}')
            for field_name in form.errors:
                getattr(form, field_name).data = ''

    return render_template('add_user.html', form=form, title="Add User")

@bp.route('/user_added', methods=['POST'])
def user_added():
    form = UserForm()
    if form.validate_on_submit():
        # Process the form data
        # print(f'got the response: {form.data}')
        dbstatus = userdb.register_user(form.data)
    else:
        print(f'Validation errors: {form.errors}')
        return redirect(url_for('main.add_user'))
    return render_template('user_added.html', status=dbstatus, form=form, title="User Added")

@bp.route('/show_user_table')
def show_user_table():
    users = userdb.get_all_users()
    users_dict = userdb.to_dict(users)
    return render_template('show_user_table.html', users=users, usersdict=users_dict, title="User Contents")