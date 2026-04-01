from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from ..forms import UserForm, DeactivateUserForm, DialogConfirm
from ..db import userdb, dis_userdb, list_tables
from ..custom_decorators import roles_required
from ..roles import Roles as roles
from flask_login import current_user



bp = Blueprint('main', __name__)
roleGroup = roles.roleGroups

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
    if form.validate_on_submit():
        dbstatus = userdb.register_user(form.data)
    else:
        print(f'Validation errors: {form.errors}')
        return redirect(url_for('main.add_user'))
    return render_template('user_added.html', status=dbstatus, form=form, title="User Added")

@bp.route('/show_user_table')
def show_user_table():
    # print (request.headers.get_all)
    users = userdb.get_all_users()
    users_dict = userdb.to_dict(users)
    return render_template('show_user_table.html', users=users, roleGroup=roleGroup, usersdict=users_dict, title="User Accounts")

@bp.route('/forward_user_id', methods=['POST'])
def forward_user_id():
    userdb.user_id = request.form.get('user_id')
    userRole = userdb.user.role # type: ignore
    redir = request.form.get('redir')
    print (f'next redirect will be {redir}')
    loggedInUserRole = current_user.role
        
    # Check if request came from JavaScript fetch
    is_ajax = request.headers.get('Accept') == 'application/json'
    if loggedInUserRole and loggedInUserRole not in roles.senior and userRole in roles.inactive:
        error_msg = "<p>The account you're trying to access is disabled.</p><p>To access or re-activate it,<br>please contact a senior staff member.</p>"
        if is_ajax:
            return jsonify({"error": error_msg})
        flash(error_msg, 'warning_modal')
        return redirect(url_for('main.show_user_table'))
    
    # Define a list of safe, allowed redirect targets and satisfy the linter!!!
    allowed_redirects = ['main.edit_user', 'main.change_password', 'main.delete_user', 'main.manage_inactive_user'] 
    if redir not in allowed_redirects:
        print ('WARNING: redirect not in allowed. Returning...')
        redir = 'main.show_user_table'
    next_url = url_for(redir)

    if is_ajax:
        return jsonify({"redirect": next_url})

    return redirect(next_url)

@bp.route('/edit_user', methods=['POST','GET'])
def edit_user():
    back_to = 'main.show_user_table'
    user = userdb.user
    if not user:
        return redirect (url_for(back_to))
    
        # columns = userdb.column_names
    form = UserForm()
    if request.method == 'POST' and form.validate_on_submit(): # POST method is when data is submitted by the user
        return render_template('added_user.html', status='Updated', form=form, title="User Edited")
    elif request.method == 'POST' and form.errors:
        print(f'Validation errors: {form.errors}')
        return redirect(url_for('main.add_user'))
    form.role.data = user.role or 'user'
    if user.role in roleGroup['inactive']:
        return redirect (url_for('main.manage_inactive_user'))
    return render_template('edit_user.html', user=user, form=form, roleGroup=roleGroup, submit_to="main.user_edited", cancel_url=back_to, title=f"Edit User: {user.username}")   #GET method
        
@bp.route('/user_edited', methods=['POST'])
def user_edited():
    form = UserForm()
    user_id = userdb.user_id
    dbstatus = userdb.update_user(form.data, user_id)
    return render_template('user_edited.html', form=form, status=dbstatus, title='User Edited')

@bp.route('/change_password', methods=['POST','GET'])
def change_password():
    back_to = 'main.edit_user'
    user = userdb.user
    if not user:
        return redirect (url_for(back_to))
    form = UserForm()
    if request.method == 'POST' and form.validate_on_submit():
        return render_template('user_password_changed.html', status="Updated", form=form, title="Password Changed")
    elif request.method == 'POST' and form.errors:
        print(f'Validation errors: {form.errors}')
        return redirect(url_for('main.edit_user'))
    return render_template('change_password.html', user=user, form=form, submit_to="main.password_changed",cancel_url=back_to, title=f"Change Password: {user.username}")

@bp.route('/password_changed', methods=['POST'])
def password_changed():
    form = UserForm()
    user_id = userdb.user_id
    dbstatus = userdb.update_password(form.data, user_id)
    return render_template ('user_password_changed.html', form=form, status=dbstatus, title="Password Update")
        

@bp.route('/delete_user', methods=['POST'])
def delete_user():
    print ('DELETE ROUTE')
    if 'user_id' in request.form:
        userdb.user_id = request.form['user_id']
    back_to = 'main.edit_user'
    user = userdb.user
    if not user:
        return redirect (url_for(back_to))
    dbstatus = userdb.delete_user(user.id)
    return render_template('user_deleted.html', status=dbstatus, title="Delete User")

@bp.route('/deactivate_user', methods=['GET','POST'])
@roles_required('super','admin')
def deactivate_user():   
    back_to = 'main.edit_user'
    user = userdb.user
    if not user:
        return redirect(url_for(back_to))
    form = DeactivateUserForm()
    # if request.method == 'POST' and form.validate_on_submit():
    #     print ('on submit')
    #     return render_template('user_deactivated.html', status="Updated", form=form, title="User Deactivated")
    return render_template('deactivate_user.html', form=form, user=user, cancel_url=back_to, title=f'Deactivate User: {user.username}')
    
@bp.route('/user_deactivated', methods=["POST"])
@roles_required('admin')
def user_deactivated():
    form = DeactivateUserForm()
    user_id = userdb.user_id
    dbstatus = userdb.deactivate_user(user_id, form.role.data, form.reason.data)
    print (f'form role is: {form.role.data} form reason is {form.reason.data}')
    return render_template('user_deactivated.html', status=dbstatus, title="User Deactivated" )

@bp.route('/manage_inactive_user')
@roles_required(*roles.roleGroups['staffers'])
def manage_inactive_user():
    user = userdb.user
    if not user:
        return redirect(url_for('main.show_user_table'))
    # userdb.reset_user_role(user)
    back_to = 'main.show_user_table'
    disabled_entry = dis_userdb.get_disabled_user_from_id(user.id)
    return render_template ('manage_inactive_user.html', user=user,disabled=disabled_entry,roleGroup=roleGroup, cancel_url=back_to, title="Manage Inactive User")
    
@bp.route('/reactivate_user', methods=['GET','POST'])
@roles_required(*roles.roleGroups['senior'])
def reactivate_user():
    form = DialogConfirm()
    user = userdb.user
    if not user:
        return redirect (url_for('main.show_user_table'))
    if request.method == 'POST' and form.validate_on_submit():
        status = userdb.reactivate_user(user.id)
        return render_template('reactivate_user.html',user=user,status=status,roleGroup=roleGroup, title=f'Reactivate User: {user.username}')    
    action_route = 'main.reactivate_user'
    return render_template('reactivate_user.html', form=form, action_route=action_route, user=user,roleGroup=roleGroup, title=f'Reactivate User: {user.username}')    

@bp.route('/demo_admin_only')
@roles_required('admin')
def demo_admin_only():
    return render_template('demo/admin_only.html', title="Admin Only")

@bp.route('/demo_role_links')
def demo_role_links():
    return render_template('demo/role_links.html', roleGroup=roleGroup, title="Check Your User Privileges")

@bp.route("/whoami")
def whoami():
    # Prefer trusted proxy/CDN headers, then fallback
    cf_ip = request.headers.get("CF-Connecting-IP")
    x_real_ip = request.headers.get("X-Real-IP")
    xff = request.headers.get("X-Forwarded-For", "")
    xff_chain = [ip.strip() for ip in xff.split(",") if ip.strip()]

    client_ip = cf_ip or x_real_ip or (xff_chain[0] if xff_chain else request.remote_addr)

    return jsonify({
        "client_ip": client_ip,
        "remote_addr": request.remote_addr,
        "x_forwarded_for": xff_chain,
        "user_agent": request.user_agent.string,
        "accept_language": request.headers.get("Accept-Language"),
    })