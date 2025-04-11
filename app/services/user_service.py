# app/services/user_service.py

from app import db
from app.models import User
from werkzeug.security import check_password_hash

# Create a new user
def create_user(email, password, goal=None, skill_level=None, preferred_style=None):
    existing_user = get_user_by_email(email)
    if existing_user:
        return None  # User already exists

    user = User(
        email=email,
        learning_goal=goal,
        skill_level=skill_level,
        preferred_style=preferred_style
    )
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user

# Fetch user by email
def get_user_by_email(email):
    return User.query.filter_by(email=email).first()

# Validate password
def check_password(user, password):
    return user.check_password(password)
