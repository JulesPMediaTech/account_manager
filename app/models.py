from sqlalchemy import func
from flask_login import UserMixin
from .extensions import db, login_manager

class User(db.Model, UserMixin): # Your User model needs to inherit from UserMixin. This adds the necessary properties for Flask-Login to manage user sessions (e.g., is_authenticated, get_id()).
    __tablename__ = 'users'
    id = db.Column(db.Integer, key="ID", primary_key=True)
    created_at = db.Column(db.DateTime, key="Created At" ,default=func.now())
    modified = db.Column(db.DateTime, key="Last Modified" ,default=func.now())
    username = db.Column(db.String(80), key="Username", index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), key="Email", index=True, unique=True)
    first_name = db.Column(db.String(80), key="First Name", nullable=False)
    last_name = db.Column(db.String(80), key="Last Name", nullable=False)
    role = db.Column(db.String(64), default='user', nullable=False)
    password_hash = db.Column(db.String(256), key="Password", nullable=False)
    
    def __repr__(self):
        return {'id':self.id,
                'username': self.username,
                'role': self.role
                }
        
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
