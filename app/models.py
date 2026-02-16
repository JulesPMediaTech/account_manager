# from sqlalchemy import Column, Integer, String, DateTime, func
# from .db import Base
from sqlalchemy import func
from .extensions import db

# class User(Base):
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, key="ID", primary_key=True)
    created_at = db.Column(db.DateTime, key="Created At" ,default=func.now())
    modified = db.Column(db.DateTime, key="Last Modified" ,default=func.now())
    username = db.Column(db.String(80), key="Username", index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), key="Email", index=True, unique=True)
    first_name = db.Column(db.String(80), key="First Name", nullable=False)
    last_name = db.Column(db.String(80), key="Last Name", nullable=False)
    role = db.Column(db.String(64), default='user', nullable=False)
    password_hash = db.Column(db.String(128), key="Password", nullable=False)
    
    def __repr__(self):
        return {'id':self.id,
                'username': self.username,
                'role': self.role
                }