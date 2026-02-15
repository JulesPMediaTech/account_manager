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
    username = db.Column(db.String(80), key="Username", unique=True, nullable=False)
    first_name = db.Column(db.String(80), key="First Name", nullable=False)
    last_name = db.Column(db.String(80), key="Last Name", nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)