from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, AnonymousUserMixin
db = SQLAlchemy()
migrate = Migrate()

class CustomAnonymousUser(AnonymousUserMixin):
    role = None  # or "guest"
    
login_manager = LoginManager()
login_manager.anonymous_user = CustomAnonymousUser


