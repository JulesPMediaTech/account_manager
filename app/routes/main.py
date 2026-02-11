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

    return render_template('add_user.html', user=None, form=form, title="Add User")

@bp.route('/user_added', methods=['POST'])
def user_added(return_to='main.index'):
    form = UserForm()
    # if form.cancel.data:
    #     print (f'CANCELLING. Returning to {return_to}')
    #     return redirect(url_for(return_to))
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
    return render_template('show_user_table.html', users=users, usersdict=users_dict, title="User Accounts")

@bp.route('/edit_user/<int:user_id>', methods=['POST','GET'])
def edit_user(user_id):
    form = UserForm()
    user = userdb.get_user_from_id(user_id)
        # columns = userdb.get_column_names()
    if request.method == 'POST' and form.validate_on_submit():
        return render_template('added_user.html', status='Updated', form=form, title="User Edited")
    elif request.method == 'POST' and form.errors:
        print(f'Validation errors: {form.errors}')
        return redirect(url_for('main.add_user'))
    return render_template('edit_user.html', user=user, form=form, return_to="main.show_user_table", title="Edit User")   #GET method
        
