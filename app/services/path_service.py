# app/services/path_service.py
"""
Service layer for handling learning path generation logic.
"""

from app import db
from app.models import User, Topic, Resource, SkillLevelEnum, ResourceTypeEnum
from sqlalchemy import case

def generate_path(user: User) -> list[Resource]:
    """
    Generates a basic, ordered learning path for a given user based on their profile.

    Args:
        user: The User object for whom to generate the path.

    Returns:
        A list of Resource objects representing the suggested learning path,
        ordered based on simple rules. Returns an empty list if required
        profile information is missing or no matching resources are found.
    """
    print(f"Generating path for user: {user.email}")
    print(f"Goal: {user.learning_goal}, Level: {user.skill_level}, Style: {user.preferred_style}")

    # --- Input Validation ---
    if not all([user.learning_goal, user.skill_level, user.preferred_style]):
        print("  User profile incomplete. Cannot generate path.")
        # Or raise a custom exception, e.g., ProfileIncompleteError
        return []

    # --- Topic Matching (Simple Name Match - Improve Later) ---
    # Attempt to find a topic that exactly matches the user's learning goal string.
    # TODO: Implement more robust goal-to-topic mapping (e.g., keyword extraction, NLP)
    target_topic = db.session.query(Topic).filter(Topic.name.ilike(user.learning_goal)).first()

    if not target_topic:
        print(f"  No topic found matching goal: '{user.learning_goal}'")
        return []
    print(f"  Matched topic: {target_topic.name} (ID: {target_topic.id})")

    # --- Difficulty Matching ---
    # The user.skill_level is already an Enum member (e.g., SkillLevelEnum.BEGINNER)
    target_difficulty = user.skill_level
    print(f"  Target difficulty: {target_difficulty.value}")


    # --- Build Query ---
    base_query = db.session.query(Resource).filter(
        Resource.topic_id == target_topic.id,
        Resource.difficulty == target_difficulty # Direct Enum comparison works
    )

    # --- Ordering Logic (Rule-Based based on Preferred Style) ---
    # Define preferred order based on style. Lower numbers come first.
    style = user.preferred_style # e.g., 'Video', 'Reading', 'Project', 'Balanced'
    ordering_preference = []

    if style == 'Video':
        ordering_preference = [
            (ResourceTypeEnum.VIDEO, 1),
            (ResourceTypeEnum.TUTORIAL, 2),
            (ResourceTypeEnum.COURSE, 3),
        ]
    elif style == 'Reading':
         ordering_preference = [
            (ResourceTypeEnum.ARTICLE, 1),
            (ResourceTypeEnum.DOCUMENTATION, 2),
            (ResourceTypeEnum.TUTORIAL, 3), # Tutorials often have text
        ]
    elif style == 'Project':
         ordering_preference = [
            (ResourceTypeEnum.PROJECT, 1),
            (ResourceTypeEnum.TUTORIAL, 2), # Tutorials often lead to projects
            (ResourceTypeEnum.ARTICLE, 3),
        ]
    # Add more specific style preferences if needed

    # Default order if 'Balanced' or no specific preference matched
    # Lower numbers = higher priority
    default_order = 100

    # Use SQLAlchemy 'case' statement to create a custom ordering column
    # Resources matching the preferred style get a lower number (higher priority)
    type_order = case(
        # Create (WHEN type = preferred_type THEN priority) clauses
        {pref_type: priority for pref_type, priority in ordering_preference},
        value=Resource.resource_type, # The column to check
        else_=default_order # Assign default priority to other types
    ).label("type_priority") # Label the resulting calculated column


    # Apply ordering: first by the calculated type priority, then by creation order/ID
    ordered_query = base_query.order_by(type_order, Resource.id) # Use ID as a stable secondary sort

    print(f"  Executing query: {ordered_query}")
    # --- Execute Query ---
    resources = ordered_query.all()

    print(f"  Found {len(resources)} matching resources.")
    return resources

# Example usage (for testing in flask shell):
# >>> from app.models import User
# >>> from app.services.path_service import generate_path
# >>> user = User.query.filter_by(email='test@example.com').first() # Get a test user
# >>> if user:
# ...     path = generate_path(user)
# ...     for resource in path:
# ...         print(f"- {resource.title} ({resource.resource_type.value})")
# ... else:
# ...     print("Test user not found.")

