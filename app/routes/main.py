from flask import Blueprint, render_template, request, redirect, url_for
from ..forms import UserForm, DeactivateUserForm
from ..db import userdb
from ..custom_decorators import roles_required
from ..roles import Roles as roles

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

    return render_template('add_user.html', user=None, form=form, submit_to="main.user_added", cancel_url="main.index", title="Add User")

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
    return render_template('show_user_table.html', users=users, roleGroup=roles.roleGroups, usersdict=users_dict, title="User Accounts")

@bp.route('/receive_user_id', methods=['POST'])
def forward_user_id():
    user_id = request.form.get('user_id')
    userdb.set_user_id(user_id)
    redir = request.form.get('redir')
    print (f'next redirect will be {redir}')
    # Define a list of safe, allowed redirect targets and satisfy the linter!!!
    allowed_redirects = ['main.edit_user', 'main.change_password', 'main.delete_user'] 
    if redir not in allowed_redirects:
        redir = 'main.show_user_table'
    return redirect(url_for(redir))

@bp.route('/edit_user', methods=['POST','GET'])
def edit_user():
    back_to = 'main.show_user_table'
    user = userdb.get_user()
    if not user:
        return redirect (url_for(back_to))
    
    form = UserForm()
        # columns = userdb.get_column_names()
    if request.method == 'POST' and form.validate_on_submit(): # POST method is when data is submitted by the user
        return render_template('added_user.html', status='Updated', form=form, title="User Edited")
    elif request.method == 'POST' and form.errors:
        print(f'Validation errors: {form.errors}')
        return redirect(url_for('main.add_user'))
    form.role.data = user.role or 'user'
    return render_template('edit_user.html', user=user, form=form, roleGroup=roles.roleGroups, submit_to="main.user_edited", cancel_url=back_to, title="Edit User")   #GET method
        
@bp.route('/user_edited', methods=['POST'])
def user_edited():
    form = UserForm()
    user_id = userdb.get_user_id()
    dbstatus = userdb.update_user(form.data, user_id)
    return render_template('user_edited.html', form=form, status=dbstatus, title='User Edited')

@bp.route('/change_password', methods=['POST','GET'])
def change_password():
    back_to = 'main.edit_user'
    user = userdb.get_user()
    if not user:
        return redirect (url_for(back_to))
    form = UserForm()
    if request.method == 'POST' and form.validate_on_submit():
        return render_template('user_password_changed.html', status="Updated", form=form, title="Password Changed")
    elif request.method == 'POST' and form.errors:
        print(f'Validation errors: {form.errors}')
        return redirect(url_for('main.edit_user'))
    return render_template('change_password.html', user=user, form=form, submit_to="main.password_changed",cancel_url=back_to, title="Change Password")

@bp.route('/password_changed', methods=['POST'])
def password_changed():
    form = UserForm()
    user_id = userdb.get_user_id()
    dbstatus = userdb.update_password(form.data, user_id)
    return render_template ('user_password_changed.html', form=form, status=dbstatus, title="Password Update")
        

@bp.route('/delete_user', methods=['POST'])
def delete_user():
    print ('DELETE ROUTE')
    if 'user_id' in request.form:
        userdb.set_user_id(request.form['user_id'])
    back_to = 'main.edit_user'
    user = userdb.get_user()
    if not user:
        return redirect (url_for(back_to))
    dbstatus = userdb.delete_user(user.id)
    return render_template('user_deleted.html', status=dbstatus, title="Delete User")

@bp.route('/deactivate_user', methods=['GET','POST'])
@roles_required('super','admin')
def deactivate_user():
    
    back_to = 'main.edit_user'
    user = userdb.get_user()
    if not user:
        return redirect(url_for(back_to))
    form = DeactivateUserForm()
    if request.method == 'POST' and form.validate_on_submit():
        return render_template('user_deactivated.html', status="Updated", form=form, title="User Deactivated")
    return render_template('deactivate_user.html', form=form, user=user, cancel_url=back_to, title='Deactivate User')
    
   
@bp.route('/user_deactivated', methods=["POST"])
@roles_required('admin')
def user_deactivated():
    form = DeactivateUserForm()
    user_id = userdb.get_user_id()
    dbstatus = userdb.deactivate_user(user_id, form.role.data)
    return render_template('user_deactivated.html', status=dbstatus, title="User Deactivated" )

@bp.route('/demo_admin_only')
@roles_required('admin')
def demo_admin_only():
    return render_template('demo/admin_only.html', title="Admin Only")

@bp.route('/demo_role_links')
def demo_role_links():
    return render_template('demo/role_links.html', roleGroup=roles.roleGroups, title="Check Your User Privileges")


    # result = userdb.delete_user(user.id)
    # if result['status'] == 'success':
    #     return redirect(url_for(back_to))
    # else:
    #     return f"Error deleting user: {result['message']}"

        
