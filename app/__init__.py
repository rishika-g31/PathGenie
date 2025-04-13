# app/__init__.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# Import other extensions later when needed
from flask_migrate import Migrate
from dotenv import load_dotenv

from flask_login import LoginManager

# from .config_default import BASE_DIR

# --- Extension Instances ---
# Initialize extensions here, but without app context initially
db = SQLAlchemy() # Create the SQLAlchemy instance
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
# login_manager = LoginManager()
# login_manager.login_view = 'auth.login'

def create_app(config_class=None):
    """
    Application Factory Function. Creates and configures the Flask app.
    """
    app = Flask(__name__, instance_relative_config=True)

    # --- Load Configuration ---
    # 1. Default config
    app.config.from_object('app.config_default')
    # 2. Instance config (overrides defaults, for secrets)
    app.config.from_pyfile('config.py', silent=True)
    # 3. Environment variables (override instance config)
    if 'SECRET_KEY' in os.environ:
        app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

    # Load DATABASE_URL from environment, map to SQLAlchemy's config key,
    # and handle 'postgres://' prefix if necessary (e.g., from Heroku).
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    elif not app.config.get('SQLALCHEMY_DATABASE_URI'):
        # Optional: Fallback if DATABASE_URL env var isn't set AND
        # SQLALCHEMY_DATABASE_URI wasn't set in config files either.
        # This uses the default defined in config_default.py
        print("Warning: DATABASE_URL environment variable not set. Using default URI from config.")

    
    
    # --- Initialize Extensions ---
    # Initialize Flask extensions with the app instance
    db.init_app(app) # Associate the db instance with the Flask app
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # --- Register Blueprints ---
    # Import and register blueprints here later
    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    from .routes.main import main_bp
    app.register_blueprint(main_bp)

    # --- Define a simple test route (optional) ---
    @app.route('/hello')
    def hello():
        # You could potentially try a simple DB query here later for testing
        return 'Hello, PathGenie World! Database should be configured.'

    # --- Return the configured app instance ---
    from . import models
    return app
