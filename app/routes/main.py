from flask import Blueprint, render_template, request, redirect, url_for
from ..forms import UserForm

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

    status = request.args.get('status', '')
    return render_template('add_user.html', status=status, form=form, title="Add User")

@bp.route('/user_added', methods=['POST'])
def user_added():
    form = UserForm()
    if form.validate_on_submit():
        # Process the form data
        print(f'got the response: {form.data}')
    else:
        print(f'Validation errors: {form.errors}')
        return redirect(url_for('main.add_user'))
    return render_template('user_added.html', form=form, title="User Added")
