# app/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from .models import SkillLevelEnum
class SignupForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match.')
    ])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

class ProfileForm(FlaskForm):
    learning_goal = TextAreaField(
        'Primary Learning Goal',
        validators=[DataRequired(), Length(min=10, max=255)],
        render_kw={"placeholder": "e.g., Learn backend development with Python and Flask, focusing on APIs and databases."}
    )

    # Populate choices from the SkillLevelEnum values
    skill_level = SelectField(
        'Current Skill Level',
        choices=[(level.value, level.value) for level in SkillLevelEnum], # Use Enum values for choices
        validators=[DataRequired()]
    )

    preferred_style = SelectField(
        'Preferred Learning Style',
        choices=[
            ('', '-- Select a Style --'), # Optional placeholder
            ('Video', 'Mostly Videos'),
            ('Reading', 'Mostly Reading/Docs'),
            ('Project', 'Project-Based'),
            ('Balanced', 'Balanced Mix')
        ],
        validators=[DataRequired()]
    )

    submit = SubmitField('Update Profile')