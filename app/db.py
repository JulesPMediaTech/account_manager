from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session

Base = declarative_base()

class DatabaseManager:
    def __init__(self):
        self.engine = None
        self.Session = None
        
    def init_db(self, database_url):
        self.engine = create_engine(database_url)
        session_factory  = sessionmaker(bind=self.engine)
        self.Session = scoped_session(session_factory)
        return self.engine
    
    def get_session(self):
        return self.Session()
    
db = DatabaseManager()


