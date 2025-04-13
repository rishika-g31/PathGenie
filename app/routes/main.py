# app/routes/main.py

from flask import Blueprint

main_bp = Blueprint('main', __name__)

@main_bp.route('/dashboard')
def dashboard():
    return "Dummy Dashboard for Testing"
