# app/services/path_service.py
"""
Service layer for handling learning path generation logic.
"""

from app import db
from app.models import User, Topic, Resource, SkillLevelEnum, ResourceTypeEnum
from sqlalchemy import case

def generate_path(user: User) -> list[Resource]:

    print(f"Generating path for user: {user.email}")
    print(f"Goal: {user.learning_goal}, Level: {user.skill_level}, Style: {user.preferred_style}")

    # --- Input Validation ---
    if not all([user.learning_goal, user.skill_level, user.preferred_style]):
        print("  User profile incomplete. Cannot generate path.")
        return []

    # --- Topic Matching (Simple Name Match - Improve Later) ---
    target_topic = db.session.query(Topic).filter(Topic.name.ilike(user.learning_goal)).first()

    if not target_topic:
        print(f"  No topic found matching goal: '{user.learning_goal}'")
        return []
    print(f"  Matched topic: {target_topic.name} (ID: {target_topic.id})")

    # --- Difficulty Matching ---
    target_difficulty = user.skill_level
    print(f"  Target difficulty Enum member: {target_difficulty}")
    print(f"  Target difficulty value for query: {target_difficulty.value}")

    # --- Build Query ---
    base_query = db.session.query(Resource).filter(
        Resource.topic_id == target_topic.id,
        Resource.difficulty == target_difficulty.value # Compare with the enum's value
    )

    # --- Ordering Logic (Rule-Based based on Preferred Style) ---
    style = user.preferred_style
    ordering_preference = []

    if style == 'Video':
        ordering_preference = [
            (ResourceTypeEnum.VIDEO, 1), (ResourceTypeEnum.TUTORIAL, 2), (ResourceTypeEnum.COURSE, 3),
        ]
    elif style == 'Reading':
         ordering_preference = [
            (ResourceTypeEnum.ARTICLE, 1), (ResourceTypeEnum.DOCUMENTATION, 2), (ResourceTypeEnum.TUTORIAL, 3),
        ]
    elif style == 'Project':
         ordering_preference = [
            (ResourceTypeEnum.PROJECT, 1), (ResourceTypeEnum.TUTORIAL, 2), (ResourceTypeEnum.ARTICLE, 3),
        ]

    default_order = 100

    # Use SQLAlchemy 'case' statement to create a custom ordering column
    type_order = case(
        # --- FIX: Use the enum's *value* as the key in the dictionary ---
        {pref_type.value: priority for pref_type, priority in ordering_preference},
        value=Resource.resource_type, # The column to check (contains strings like 'Video')
        else_=default_order
    ).label("type_priority")

    # Apply ordering: first by the calculated type priority, then by creation order/ID
    ordered_query = base_query.order_by(type_order, Resource.id)

    print(f"  Executing query: {ordered_query}")
    # --- Execute Query ---
    try:
        resources = ordered_query.all()
        print(f"  Found {len(resources)} matching resources.")
        return resources
    except Exception as e:
        print(f"  Error executing query: {e}")
        # Log the error appropriately
        # raise e # Or re-raise if needed
        return []


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

