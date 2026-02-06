from flask import Blueprint, render_template, request, redirect, url_for
from ..forms import UserForm

bp = Blueprint('main', __name__)

@bp.route('/')
def home():
    return redirect(url_for('main.index'))

@bp.route('/index', methods=['GET', 'POST'])
def index():
    status = request.args.get('status', '')
    return render_template('index.html', status=status)

@bp.route('/add_user', methods=['GET','POST'])
def add_user():
    form = UserForm()
    if form.validate_on_submit():
        print(f'got the response: {form.data}')
    else:
        if request.method == 'POST' and form.errors:
            print(f'validation errors: {form.errors}')
            for field_name in form.errors:
                getattr(form, field_name).data = ''

    status = request.args.get('status', '')
    return render_template('add_user.html', status=status, form=form)

# @bp.route('/submit', methods=['POST'])
# def handle_data():
#     username = request.form.get('user-id')
#     print(f'username: {username}')
#     if username:
#         return f"Hello, {username}!"
#     return "Invalid Data", 400