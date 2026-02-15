# from sqlalchemy import create_engine
from sqlalchemy import select, inspect, func
from sqlalchemy.exc import SQLAlchemyError
from .extensions import db
from .models import User
# from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session

# Base = declarative_base()
# from .models import db

class UserDatabase:
    # def __init__(self):
    #     self.engine = None
    #     self.Session = None
        
    # def init_db(self, database_url):
    #     self.engine = create_engine(database_url)
    #     session_factory  = sessionmaker(bind=self.engine)
    #     self.Session = scoped_session(session_factory)
    #     return self.engine
    
    # def get_session(self):
    #     return self.Session()
    
    def field_map(self):
        return {
            # form key : model attribute
            "username": "username",
            "firstName": "first_name",
            "lastName": "last_name",
            "password" : "password_hash"
    }
    
    def register_user(self, data):
        print (f'DB Received data: {data}')
        # session = self.get_session()
        try:
            user = User()
            filled = 0
            # add user data fields to database model using field_map
            for form_key, model_attr in self.field_map().items():
                if data[form_key]:
                    setattr(user, model_attr, data[form_key])
                    filled += 1
            if filled: 
                db.session.add(user)
                db.session.commit()
                return {'status': 'success', 'user_id': user.id}
            else:
                return {"status": "nothing-added", "message": "no data was filled"}
        except Exception as e:
            db.session.rollback()
            return {'status': 'error', 'message': str(e)}
        
    def set_user_id(self, id):
        self.id = id
        
    def get_user_id(self):
        return getattr(self, 'id', None)
        
    def update_user(self,data,id):
        try:
            stmt = db.select(User).where(User.id == id)
            user = db.session.execute(stmt).scalar_one()
            
            # password doesn't get updated here (it's blank) so remove it from data form
            field_map = self.field_map()
            del field_map['password']
            
            changed = 0
            for form_key, model_attr in field_map.items():
                if form_key in data and data[form_key] != getattr(user,model_attr):
                    setattr(user, model_attr, data[form_key])
                    changed += 1
            if changed:
                user.modified = func.now()
                db.session.commit()
                return {"status": f"success ({changed}) entry changed","user_id" : user.id }
            return {"status": "no-changes", "message": "no data was changed"}
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"status": "error","message" : str(e) }
        
    def update_password(self,data,id):
        try: 
            stmt = db.select(User).where(User.id == id)
            user = db.session.execute(stmt).scalar_one()
            if data['password'] != '' and data['password'] != user.password_hash :
                user.password_hash = data['password']
                user.modified = func.now()
                db.session.commit()
                return {"status": "success! Password changed","user_id" : user.id }
            return {"status": "no-changes", "message": "password unchanged"}
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"status": "error","message" : str(e) }
                
    def delete_user(self, id):
        try:
            user = self.get_user_from_id(id)
            if user:
                db.session.delete(user)
                db.session.commit()
                return {"status": "success! User deleted","User" : user }
            return {"status": "error", "message": "User not found"}
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"status": "error","message" : str(e) }
            

            
            
    def get_all_users(self):
        # session = self.get_session()
        # 1. Create the select statement
        stmt = select(User)
        # 2. Execute and return scalar results (the User objects)
        users = db.session.scalars(stmt).all()
        return users
    
    def get_user_from_id(self, id):
        stmt = select(User).where(User.id == id)
        user = db.session.scalar(stmt)
        return user
    
    def get_user(self):
        user_id = self.get_user_id()
        if not user_id:
            return None
        return self.get_user_from_id(user_id)
    
        

    
    def get_column_names(self):
        return User.__table__.columns # type: ignore
        
    def to_dict(self,obj):
        users = []
        for user in obj:
            users.append({c.key: getattr(user, c.key) for c in inspect(user).mapper.column_attrs})
        return users
            
            
    
userdb = UserDatabase()


