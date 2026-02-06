from flask import Flask
from flask_wtf.csrf import CSRFProtect
from .config import Config
from .db import db, Base
from . import models  # ensure model registration
from .routes.main import bp as main_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Init DB
    db.init_db(app.config["DATABASE_URL"])
    with app.app_context():
        Base.metadata.create_all(bind=db.engine)

    # CSRF
    CSRFProtect(app)

    # Blueprints
    app.register_blueprint(main_bp)

    print("Running Account Manager Server...")
    return app
