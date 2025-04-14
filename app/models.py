# app/models.py

import enum 
from datetime import datetime, timezone
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy import String

class ResourceTypeEnum(enum.Enum):
    ARTICLE = "Article"
    VIDEO = "Video"
    COURSE = "Course"
    DOCUMENTATION = "Documentation"
    PROJECT = "Project"
    TUTORIAL = "Tutorial"
    OTHER = "Other"

class DifficultyLevelEnum(enum.Enum):
    BEGINNER = "Beginner"
    INTERMEDIATE = "Intermediate"
    ADVANCED = "Advanced"
    ALL_LEVELS = "All Levels"


class SkillLevelEnum(enum.Enum):
    BEGINNER = "Beginner"
    INTERMEDIATE = "Intermediate"
    ADVANCED = "Advanced"

# class ProgressStatusEnum(enum.Enum):
#     NOT_STARTED = "Not Started"
#     IN_PROGRESS = "In Progress"
#     COMPLETED = "Completed"

# --- Define Models ---

# class User(UserMixin, db.Model): # If using Flask-Login
class User(UserMixin,db.Model):
   
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(512), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Profile information
    learning_goal = db.Column(db.String(255), nullable=True)
    # --- Updated skill_level to use Enum ---
    skill_level = db.Column(db.Enum(SkillLevelEnum, values_callable=lambda obj: [e.value for e in obj]),
                            nullable=True, # Allow null until user sets profile
                            name="skill_level_enum")
    preferred_style = db.Column(db.String(50), nullable=True)

    # --- Relationships ---
    # Define relationship to the UserResourceProgress association table
    # Use back_populates for clearer bidirectional relationship definition
    # progress = db.relationship('UserResourceProgress', back_populates='user', cascade="all, delete-orphan")

    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        skill_str = self.skill_level.value if self.skill_level else 'N/A'
        return f"<User {self.email} (Skill: {skill_str})>"


class Topic(db.Model):
    """
    Represents a learning topic (e.g., Python, Flask, Data Analysis).
    """
    __tablename__ = 'topics'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False, index=True)

    # --- Relationships ---
    resources = db.relationship('Resource', backref='topic', lazy='dynamic') # Changed lazy to dynamic for potential filtering

    def __repr__(self):
        return f"<Topic {self.name}>"


class Resource(db.Model):
    """
    Represents a learning resource (e.g., article, video, course).
    Uses Enums for resource_type and difficulty.
    """
    __tablename__ = 'resources'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(512), nullable=False, unique=True)

    # --- Enum Fields ---
    resource_type = db.Column(db.Enum(ResourceTypeEnum, values_callable=lambda obj: [e.value for e in obj]),
                              nullable=False,
                              name="resource_type_enum")
    difficulty = db.Column(db.Enum(DifficultyLevelEnum, values_callable=lambda obj: [e.value for e in obj]),
                           nullable=False,
                           name="difficulty_level_enum")

    # --- Other Fields ---
    estimated_time = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # --- Foreign Keys ---
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'), nullable=False)

    # --- Relationships ---
    # Define relationship to the UserResourceProgress association table
    # user_progress = db.relationship('UserResourceProgress', back_populates='resource', cascade="all, delete-orphan")


    def __repr__(self):
        return f"<Resource {self.title[:50]} ({self.resource_type.value}, {self.difficulty.value})>"


# --- Added UserResourceProgress Model ---
# class UserResourceProgress(db.Model):
#     """
#     Association table to track user progress on resources (Many-to-Many).
#     Uses Enum for status.
#     """
#     __tablename__ = 'user_resource_progress'

#     # Composite primary key
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
#     resource_id = db.Column(db.Integer, db.ForeignKey('resources.id'), primary_key=True)

#     # Progress tracking fields
#     status = db.Column(db.Enum(ProgressStatusEnum, values_callable=lambda obj: [e.value for e in obj]),
#                        nullable=False,
#                        default=ProgressStatusEnum.NOT_STARTED, # Default status
#                        name="progress_status_enum")
#     started_at = db.Column(db.DateTime, nullable=True)
#     completed_at = db.Column(db.DateTime, nullable=True) # Timestamp when completed

#     # --- Relationships ---
#     # Define relationships back to User and Resource using back_populates
#     user = db.relationship('User', back_populates='progress')
#     resource = db.relationship('Resource', back_populates='user_progress')

#     def __repr__(self):
#         return f"<Progress User {self.user_id} - Resource {self.resource_id} ({self.status.value})>"

