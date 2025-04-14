# app/routes/main.py
"""
Main routes for the PathGenie application (dashboard, profile, path display).
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user # Assuming Flask-Login is setup
from app import db
from app.models import User, SkillLevelEnum, Resource # Import Resource model
from app.forms import ProfileForm # Import the profile form
from app.services.path_service import generate_path # Import path generation service

# Create a Blueprint for main routes
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@main_bp.route('/dashboard')
@login_required # Protect this route
def dashboard():
    """Displays the user's dashboard."""
    # Check if user profile is complete to provide relevant prompts
    profile_complete = all([current_user.learning_goal, current_user.skill_level, current_user.preferred_style])
    return render_template(
        'main/dashboard.html',
        title='Dashboard',
        profile_complete=profile_complete # Pass completion status to template
    )

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
            # Convert the string value from the form back to an Enum member
            current_user.skill_level = SkillLevelEnum(selected_skill_value)
        except ValueError:
            flash('Invalid skill level selected.', 'danger')
            # Keep existing value or set to None if invalid selection occurs
            pass # Or handle more gracefully, e.g., don't update field

        current_user.preferred_style = form.preferred_style.data

        try:
            db.session.commit()
            flash('Your profile has been updated!', 'success')
            return redirect(url_for('main.learning_path')) 
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


# --- Route for Displaying Learning Path ---
@main_bp.route('/path')
@login_required # Protect this route
def learning_path():
    """Generates and displays the user's learning path."""

    # Check if profile is complete before attempting generation
    profile_complete = all([current_user.learning_goal, current_user.skill_level, current_user.preferred_style])
    if not profile_complete:
        flash('Please complete your profile first to generate a learning path.', 'warning')
        return redirect(url_for('main.profile')) # Redirect user to profile page

    # Call the service function to get the path
    try:
        # Pass the current_user object to the generation service
        path = generate_path(current_user)
        # 'path' will be a list of Resource objects or an empty list
    except Exception as e:
        # Log the error properly in a real application
        print(f"Error generating path for user {current_user.id}: {e}")
        flash('An error occurred while generating your learning path. Please try again later.', 'danger')
        path = [] # Ensure path is an empty list on error

    # Render the path template, passing the list of resources
    return render_template('main/path.html', title='Your Learning Path', path=path)

