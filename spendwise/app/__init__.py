from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message_category = "warning"


def create_app(config_class=Config):
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)

    from app.routes.auth import auth_bp
    from app.routes.main import main_bp
    from app.routes.expenses import expenses_bp
    from app.routes.income import income_bp
    from app.routes.reports import reports_bp
    from app.routes.profile import profile_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(expenses_bp)
    app.register_blueprint(income_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(profile_bp)

    # Create instance directory for SQLite database if needed
    with app.app_context():
        import os
        instance_path = os.path.join(app.instance_path)
        if not os.path.exists(instance_path):
            os.makedirs(instance_path, exist_ok=True)
        
        # Auto-initialize database tables if they don't exist
        from app.models import user, expense, income  # noqa: F401
        with app.app_context():
            db.create_all()
    from app.models import user, expense, income  # just import models

    return app
