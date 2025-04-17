# app/__init__.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate       # Assuming Migrate is initialized
from flask_login import LoginManager   # Assuming LoginManager is initialized
from datetime import datetime, timezone # Import datetime utilities

db = SQLAlchemy()
migrate = Migrate() # Initialize Migrate instance
login_manager = LoginManager() # Initialize LoginManager instance
login_manager.login_view = 'auth.login' # Set login view endpoint

# --- User Loader Callback (Required for Flask-Login) ---
# It's often cleaner to define this outside create_app but ensure it's registered
@login_manager.user_loader
def load_user(user_id):
    # Import inside the function to avoid circular imports during init
    from .models import User
    # Use session.get for primary key lookup
    return db.session.get(User, int(user_id))


def create_app(config_class=None):
    """
    Application Factory Function. Creates and configures the Flask app.
    """
    app = Flask(__name__, instance_relative_config=True)

    # --- Load Configuration ---
    app.config.from_object('app.config_default')
    app.config.from_pyfile('config.py', silent=True)


    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    elif not app.config.get('SQLALCHEMY_DATABASE_URI'):
        print("Warning: DATABASE_URL environment variable not set. Using default URI from config.")

    # if 'SECRET_KEY' in os.environ:
    #     app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    # elif not app.config.get('SECRET_KEY'):
    #      print("Warning: SECRET_KEY not found in environment or config files. Using default.")


    groq_api_key = os.environ.get('GROQ_API_KEY')
    if groq_api_key:
        app.config['GROQ_API_KEY'] = groq_api_key
    elif not app.config.get('GROQ_API_KEY'):
         print("Warning: GROQ_API_KEY not found in environment or config files. Using default.")
        
    # --- Initialize Extensions ---
    db.init_app(app)
    migrate.init_app(app, db) # Pass db instance to Migrate
    login_manager.init_app(app)


    # --- Context Processor (Injects variables into all templates) ---
    @app.context_processor
    def inject_now():
        """Injects the current UTC datetime into template context."""
        return {'now': datetime.now(timezone.utc)}
    # --- End of Context Processor ---


    # --- Register Blueprints ---
    # Import blueprints inside the factory function to avoid circular imports
    from .routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from .routes.main import main_bp
    app.register_blueprint(main_bp)

    from .routes.chat import chat_bp
    app.register_blueprint(chat_bp)

    # --- Define a simple test route (optional) ---
    @app.route('/hello')
    def hello():
        return 'Hello, PathGenie World! Database should be configured.'

    # --- Return the configured app instance ---
    return app

