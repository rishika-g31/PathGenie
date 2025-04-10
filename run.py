# run.py
"""
Entry point script to run the PathGenie Flask application.
This script imports the create_app function from the application package
and runs the development server.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file *before* creating the app
# This ensures that FLASK_ENV, FLASK_DEBUG, SECRET_KEY, DATABASE_URL etc. are available
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
    print("Loaded environment variables from .env")
else:
    print("Warning: .env file not found.")


# Now import the app factory from your application package
from app import create_app

# Create the Flask app instance using the factory
# You could potentially pass a specific config class here if needed,
# e.g., create_app('app.config_testing.TestingConfig')
app = create_app()

if __name__ == '__main__':
    # Run the Flask development server
    # Debug mode is typically controlled by FLASK_DEBUG environment variable loaded from .env
    # Host '0.0.0.0' makes the server accessible externally (e.g., within a Docker container or local network)
    # Use host '127.0.0.1' (default) to only allow connections from the local machine.
    # Port can be changed if 5000 is already in use.
    app.run(host='0.0.0.0', port=5000)

