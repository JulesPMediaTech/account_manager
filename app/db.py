# from sqlalchemy import create_engine
from sqlalchemy import select, inspect
# from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session

# Base = declarative_base()
from .models import db

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
    
    def register_user(self, data):
        from .models import User
        print (f'DB Received data: {data}')
        # session = self.get_session()
        try:
            user = User (
                username = data['username'],
                first_name = data['firstName'],
                last_name = data['lastName'],
                password_hash = data['password']
            )
            db.session.add(user)
            db.session.commit()
            user_id = user.id
            db.session.close()
            return {'status': 'success', 'user_id': user_id}
        except Exception as e:
            db.session.rollback()
            db.session.close()
            return {'status': 'error', 'message': str(e)}
            
            
    def get_all_users(self):
        from .models import User
        # session = self.get_session()
        # 1. Create the select statement
        stmt = select(User)
        # 2. Execute and return scalar results (the User objects)
        users = db.session.scalars(stmt).all()
        return users
        
    def to_dict(self,obj):
        users = []
        for user in obj:
            users.append({c.key: getattr(user, c.key) for c in inspect(user).mapper.column_attrs})
        return users
            
            
    
userdb = UserDatabase()


