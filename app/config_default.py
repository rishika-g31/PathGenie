# app/config_default.py
"""
Default configuration settings for the PathGenie application.
These settings are common across all environments (development, testing, production)
or provide sensible defaults that can be overridden.
"""

import os

# Get the base directory of the application
# This helps in defining paths relative to the project root
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# --- Core Flask Settings ---

# Enable/Disable debug mode. Should be False in production.
# Overridden by environment variable FLASK_DEBUG if set.
DEBUG = False

# Enable/Disable testing mode.
TESTING = False

# Secret key for session management, CSRF protection, etc.
# IMPORTANT: This is just a default placeholder.
# A strong, unique secret key MUST be set in instance/config.py or via environment variable.
# You can generate one using: python -c 'import secrets; print(secrets.token_hex(16))'
SECRET_KEY = 'default-insecure-secret-key-please-change'

# --- Database Settings ---

# Default database URI (using SQLite for easy default setup)
# This will typically be overridden in instance/config.py or by DATABASE_URL env var
# for PostgreSQL in development/production.
# Example for SQLite: 'sqlite:///' + os.path.join(BASE_DIR, 'instance', 'app.db')
# Example for PostgreSQL: 'postgresql://user:password@host:port/dbname'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'instance', 'app.db')

# Disable SQLAlchemy event system if not needed, can improve performance.
SQLALCHEMY_TRACK_MODIFICATIONS = False

# --- Add other default settings as needed ---
# e.g., Mail server settings, API keys (use env vars for secrets!)

