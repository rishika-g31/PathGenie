# app/routes/main.py

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user # Assuming Flask-Login is setup
from app import db
from app.models import User, SkillLevelEnum # Import User model and Enum
from app.forms import ProfileForm # Import the new form

# Create a Blueprint for main routes
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@main_bp.route('/dashboard')
@login_required # Protect this route
def dashboard():
    """Displays the user's dashboard."""
    # Placeholder: Add logic later to show progress, suggested next steps, etc.
    return render_template('main/dashboard.html', title='Dashboard')

@main_bp.route('/profile', methods=['GET', 'POST'])
@login_required # Protect this route
def profile():
    """Displays and handles updates for the user's profile."""
    form = ProfileForm()

    if form.validate_on_submit():
        # Process the submitted form data
        current_user.learning_goal = form.learning_goal.data

        # Find the correct SkillLevelEnum member based on the form's string value
        selected_skill_value = form.skill_level.data
        try:
            current_user.skill_level = SkillLevelEnum(selected_skill_value)
        except ValueError:
            flash('Invalid skill level selected.', 'danger')
            # You might want to handle this more gracefully
            # For now, we'll just not update it if the value is somehow invalid
            pass

        current_user.preferred_style = form.preferred_style.data

        try:
            db.session.commit()
            flash('Your profile has been updated!', 'success')
            return redirect(url_for('main.profile')) # Redirect back to profile page
        except Exception as e:
            db.session.rollback() # Rollback in case of error
            flash(f'Error updating profile: {e}', 'danger')

    elif request.method == 'GET':
        # Pre-populate the form with existing data when the page loads
        form.learning_goal.data = current_user.learning_goal
        # Pre-select the correct enum value if it exists
        if current_user.skill_level:
            form.skill_level.data = current_user.skill_level.value # Set form data to the enum's value
        form.preferred_style.data = current_user.preferred_style

    return render_template('main/profile.html', title='Edit Profile', form=form)

# Add other main routes here later (e.g., for displaying the learning path)

