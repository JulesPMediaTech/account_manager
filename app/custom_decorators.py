from flask_login import current_user
from flask import abort

def roles_required(*roles):
    from functools import wraps
    def wrapper(f):
        @wraps(f)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role not in roles:
                return abort(403)  # Or redirect to a specific page
            return f(*args, **kwargs)
        return decorated_view
    return wrapper