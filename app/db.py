# from sqlalchemy import create_engine
from sqlalchemy import select, inspect, func
from sqlalchemy.exc import SQLAlchemyError
from .extensions import db
from .models import User, InactiveUser
from werkzeug.security import generate_password_hash
# from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session

# Base = declarative_base()
# from .models import db


def list_tables():
    inspector = inspect(db.engine)
    return inspector.get_table_names()

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
    
    @property
    def table_exists(self):
        inspector = inspect(db.engine)
        return inspector.has_table('users')
    
    def field_map(self):
        return {
            # form key : model attribute
            "username": "username",
            "email" : "email",
            "firstName": "first_name",
            "lastName": "last_name",
            "role" : "role",
            "password" : "password_hash"
    }
    
    def register_user(self, data):
        print (f'DB Received data: {data}')
        try:
            user = User()
            filled = 0
            # add user data fields to database model using field_map
            for form_key, model_attr in self.field_map().items():
                if form_key in data and data[form_key]:
                    # Hash password if the key is 'password'
                    if form_key == 'password':
                        setattr(user, model_attr, generate_password_hash(data[form_key]))
                    else:
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
        
    @property
    def user_id(self):
        return getattr(self,'id',None)
    
    @user_id.setter
    def user_id(self,id):
        self.id = id
                
    def update_user(self,data,id):
        try:
            stmt = db.select(User).where(User.id == id)
            user = db.session.execute(stmt).scalar_one()
            
            # password doesn't get updated here (it's blank) so remove it from data form
            field_map = self.field_map()
            if 'password' in field_map:
                del field_map['password']
            
            changed = 0
            for form_key, model_attr in field_map.items():
                model_data = getattr(user,model_attr)
                if form_key in data and data[form_key] != model_data and data[form_key]:
                    setattr(user, model_attr, data[form_key])
                    changed += 1
                # if model_data == '' or not model_data: 
                #     setattr(user, model_attr, None)
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
            # Note: We can't compare plain text to hash easily here without check_password_hash
            # For now, we just check if it's not empty. Login logic will handle verification later.
            if data['password'] != '':
                user.password_hash = generate_password_hash(data['password'])
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
        
    def reset_user_role(self,user):
        if user:
            user.role = 'user'
            db.session.commit()
            return {"status" : "success! User role set to user"}
        return {"status": "error", "message": "User not found"}
        
    def deactivate_user(self, id, inactive_role, reason):
        userdb_status = {"status": "error", "message": "User not found"}
        dis_status = {"status": "error", "message": "not executed due to userdb error"}
        try:
            user = self.get_user_from_id(id)
            if user:
                dis_status = dis_userdb.add_to_deactivated_db(user,inactive_role,reason)
                user.role = inactive_role
                db.session.commit()
                userdb_status = {'status': f'success! User deactivated with role {inactive_role}'}
        except SQLAlchemyError as e:
            db.session.rollback()
            userdb_status =  {"status": "error","message" : str(e) }
        return {'userDB status' : userdb_status, 'inactiveDB status' : dis_status}
    
    def reactivate_user(self, id):
        userdb_status = {"status": "error", "message": "User not found"}
        dis_status = {"status": "error", "message": "not executed due to userdb error"}      
        try:
            user = self.get_user_from_id(id)
            if user:
                dis_user = dis_userdb.get_disabled_user_from_id(id)
                user.role = dis_user.active_role     #type: ignore
                db.session.commit()
                userdb_status = {'status': f'success! User re-activated with role {user.role}'}
                dis_status = dis_userdb.remove_from_deactivated_db(dis_user)
        except SQLAlchemyError as e:
            db.session.rollback()
            userdb_status =  {"status": "error","message" : str(e) }
        return {'userDB status' : userdb_status, 'inactiveDB status' : dis_status}
            
        
            
    def get_all_users(self):
        # 1. Create the select statement
        stmt = select(User)
        # 2. Execute and return scalar results (the User objects)
        users = db.session.scalars(stmt).all()
        return users
    
    def get_user_from_id(self, id):
        stmt = select(User).where(User.id == id)
        user = db.session.scalar(stmt)
        return user
    
    @property
    def user(self):
        user_id = getattr(self, 'user_id', None)
        return self.get_user_from_id(user_id) if user_id else None    
        
    @property
    def column_names(self):
        return User.__table__.columns # type: ignore
                
    def to_dict(self,obj):
        users = []
        for user in obj:
            users.append({c.key: getattr(user, c.key) for c in inspect(user).mapper.column_attrs})
        return users
                   
    
userdb = UserDatabase()


''' Disabled Deactivated User Database methods '''
class DisabledUserDB():
    
    @property
    def table_exists(self):
        inspector = inspect(db.engine)
        return inspector.has_table('inactive_users')

    
    def add_to_deactivated_db(self,user,inactive_role,reason):
        from flask_login import current_user
        try:
            disUser = InactiveUser()
            disUser.id = user.id
            disUser.username = user.username
            disUser.active_role = user.role
            disUser.inactive_role = inactive_role
            disUser.staff_username = current_user.username
            disUser.reason = reason
            db.session.add(disUser)
            db.session.commit()
            return {'status': 'success', 'disUser_id': disUser.id}
        except Exception as e:
            db.session.rollback()
            return {"status" : "failed to update disabled user db", "error" : str(e)}
        
    def remove_from_deactivated_db(self,dis_user_entry):
        try:
            print (f'removing from inactive_db: {dis_user_entry.username}')
            db.session.delete(dis_user_entry)
            db.session.commit()
            return {"status": "success! Removed disabled entry for user", "User": dis_user_entry }
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"status": "error", "message" : str(e)}
        
    def get_disabled_user_from_id(self,user_id):
        stmt = select(InactiveUser).where(InactiveUser.id == user_id)
        user = db.session.scalar(stmt)
        return user

            
        

dis_userdb = DisabledUserDB()
        
        