from flask import Flask, render_template
from flask_wtf.csrf import CSRFProtect, CSRFError
from .config import Config
# from .db import db, Base
from .extensions import db as fdb, migrate
from . import models  # ensure models are imported
from .routes.main import bp as main_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    print("WTF_CSRF_TIME_LIMIT =", app.config.get("WTF_CSRF_TIME_LIMIT"))
    

    # Init DB
    fdb.init_app(app)
    migrate.init_app(app, fdb)
    
    # db.init_db(app.config["DATABASE_URL"])
    # with app.app_context():
    #     Base.metadata.create_all(bind=db.engine)

    # CSRF
    CSRFProtect(app)

    # Blueprints
    app.register_blueprint(main_bp)

    print("Running Account Manager Server...")
    
    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        return render_template('csrf_error.html', reason=e.description), 400

    return app