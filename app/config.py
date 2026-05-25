import os
from dotenv import load_dotenv

# Load .env for local use
load_dotenv()

def read_secret(env_var, file_path):
    secret = os.getenv(env_var)
    if not secret:
        with open(file_path, 'r') as f:
            secret = f.read().strip()
    return secret

class Config:
    SECRET_KEY = read_secret("SECRET_KEY", "/app/secrets/secret_key")
    DB_PASSWORD = read_secret("DB_PASSWORD", "/app/secrets/db_password")
    DATABASE_URL = f"postgresql://accmanager:{DB_PASSWORD}@postgres:5432/accmanager_db"
    SQLALCHEMY_DATABASE_URI = f"postgresql://accmanager:{DB_PASSWORD}@postgres:5432/accmanager_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # WTF_CSRF_TIME_LIMIT = 5 # set CSRF token expiry to 5 secs for testing error handling