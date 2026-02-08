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
    SECRET_KEY = read_secret("SECRET_KEY", "/run/secrets/secret_key")
    DB_PASSWORD = read_secret("DB_PASSWORD", "/run/secrets/db_password")
    DATABASE_URL = f"postgresql://accmanager:{DB_PASSWORD}@postgres:5432/accmanager_db"
    SQLALCHEMY_DATABASE_URI = f"postgresql://accmanager:{DB_PASSWORD}@postgres:5432/accmanager_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # WTF_CSRF_TIME_LIMIT = 5 # 5 seconds CSRF token expiry for testing