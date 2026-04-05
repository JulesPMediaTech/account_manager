from flask import Flask, render_template
from flask_wtf.csrf import CSRFProtect, CSRFError
from .config import Config
from .extensions import db as fdb, migrate, login_manager
from . import models  # ensure models are imported
from .routes.main import bp as main_bp
from .routes.auth import auth_bp
from datetime import datetime
from .roles import Roles

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)
    print("WTF_CSRF_TIME_LIMIT =", app.config.get("WTF_CSRF_TIME_LIMIT"))


    # Init DB
    fdb.init_app(app)
    migrate.init_app(app, fdb)
    
    # Init LoginManager
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # type: ignore # The route to redirect to for login @login_required

    
    
    # CSRF
    CSRFProtect(app)

    # Blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    
    # Context Processor - injects variables to ALL templates
    @app.context_processor
    def global_template_variables():
        return {'now' : datetime.now(),
                'roleGroup' : Roles.roleGroups}

    print("Running Account Manager Server...")
    
    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        return render_template('errors/csrf_error.html', reason=e.description), 400
    
    @app.errorhandler(403)
    def handle_forbidden(e):
        return render_template('errors/forbidden_error.html', reason=e.description), 403
    
    return app
