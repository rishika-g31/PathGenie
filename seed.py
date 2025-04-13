# seed.py

import os
from app import create_app, db # Import app factory and db instance
from app.models import Topic, Resource, ResourceTypeEnum, DifficultyLevelEnum # Import models and enums

# Sample Data Definition
# You can expand this list significantly
SAMPLE_TOPICS = [
    "Python Basics",
    "Flask Framework",
    "SQLAlchemy ORM",
    "HTML & CSS",
    "JavaScript Fundamentals"
]

SAMPLE_RESOURCES = [
    # Python Basics
    {
        "title": "Official Python Tutorial (docs.python.org)",
        "url": "https://docs.python.org/3/tutorial/",
        "resource_type": ResourceTypeEnum.DOCUMENTATION,
        "difficulty": DifficultyLevelEnum.BEGINNER,
        "topic_name": "Python Basics"
    },
    {
        "title": "Learn Python - Full Course for Beginners [Tutorial]",
        "url": "https://www.youtube.com/watch?v=rfscVS0vtbw", # freeCodeCamp.org example URL
        "resource_type": ResourceTypeEnum.VIDEO,
        "difficulty": DifficultyLevelEnum.BEGINNER,
        "topic_name": "Python Basics"
    },
    {
        "title": "Automate the Boring Stuff with Python (Book)",
        "url": "https://automatetheboringstuff.com/",
        "resource_type": ResourceTypeEnum.ARTICLE, # Technically a book/website
        "difficulty": DifficultyLevelEnum.INTERMEDIATE,
        "topic_name": "Python Basics"
    },
    # Flask Framework
    {
        "title": "Flask Mega-Tutorial (Miguel Grinberg)",
        "url": "https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world",
        "resource_type": ResourceTypeEnum.TUTORIAL,
        "difficulty": DifficultyLevelEnum.INTERMEDIATE,
        "topic_name": "Flask Framework"
    },
    {
        "title": "Flask Official Documentation - Quickstart",
        "url": "https://flask.palletsprojects.com/en/latest/quickstart/",
        "resource_type": ResourceTypeEnum.DOCUMENTATION,
        "difficulty": DifficultyLevelEnum.BEGINNER,
        "topic_name": "Flask Framework"
    },
    {
        "title": "Build a SAAS App with Flask (Course Example)",
        "url": "https://testdriven.io/courses/learn-flask/", # Example course URL
        "resource_type": ResourceTypeEnum.COURSE,
        "difficulty": DifficultyLevelEnum.ADVANCED,
        "topic_name": "Flask Framework"
    },
    # SQLAlchemy ORM
    {
        "title": "SQLAlchemy ORM Tutorial (Official Docs)",
        "url": "https://docs.sqlalchemy.org/en/latest/orm/tutorial.html",
        "resource_type": ResourceTypeEnum.DOCUMENTATION,
        "difficulty": DifficultyLevelEnum.INTERMEDIATE,
        "topic_name": "SQLAlchemy ORM"
    },
    {
        "title": "Using SQLAlchemy with Flask (RealPython)",
        "url": "https://realpython.com/flask-sqlalchemy-database/",
        "resource_type": ResourceTypeEnum.ARTICLE,
        "difficulty": DifficultyLevelEnum.INTERMEDIATE,
        "topic_name": "SQLAlchemy ORM"
    },
    # HTML & CSS
    {
        "title": "MDN Web Docs - HTML Basics",
        "url": "https://developer.mozilla.org/en-US/docs/Learn/Getting_started_with_the_web/HTML_basics",
        "resource_type": ResourceTypeEnum.DOCUMENTATION,
        "difficulty": DifficultyLevelEnum.BEGINNER,
        "topic_name": "HTML & CSS"
    },
    {
        "title": "CSS Tutorial (W3Schools)",
        "url": "https://www.w3schools.com/css/default.asp",
        "resource_type": ResourceTypeEnum.TUTORIAL,
        "difficulty": DifficultyLevelEnum.BEGINNER,
        "topic_name": "HTML & CSS"
    },
     # JavaScript Fundamentals
    {
        "title": "MDN Web Docs - JavaScript Guide",
        "url": "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide",
        "resource_type": ResourceTypeEnum.DOCUMENTATION,
        "difficulty": DifficultyLevelEnum.BEGINNER,
        "topic_name": "JavaScript Fundamentals"
    },
    {
        "title": "Eloquent JavaScript (Book/Website)",
        "url": "https://eloquentjavascript.net/",
        "resource_type": ResourceTypeEnum.ARTICLE, # Book/Website
        "difficulty": DifficultyLevelEnum.INTERMEDIATE,
        "topic_name": "JavaScript Fundamentals"
    }
]


def seed_database():
    """Seeds the database with sample topics and resources."""
    app = create_app()
    with app.app_context():
        print("Seeding database...")

        # --- WARNING: Optional - Clear existing data ---
        # Uncomment the following lines if you want the script to delete all
        # existing resources and topics before seeding. Use with caution!
        # print("Clearing existing Resource and Topic data...")
        # db.session.query(Resource).delete()
        # db.session.query(Topic).delete()
        # db.session.commit()
        # print("Existing data cleared.")
        # --- End of Optional Clear ---

        # --- Seed Topics ---
        existing_topics = {topic.name: topic for topic in db.session.query(Topic).all()}
        topics_to_add = []
        for topic_name in SAMPLE_TOPICS:
            if topic_name not in existing_topics:
                new_topic = Topic(name=topic_name)
                topics_to_add.append(new_topic)
                existing_topics[topic_name] = new_topic # Add to dict for resource linking
                print(f"  Preparing Topic: {topic_name}")

        if topics_to_add:
            db.session.add_all(topics_to_add)
            db.session.commit() # Commit topics first to ensure they have IDs
            print(f"Added {len(topics_to_add)} new topics.")
        else:
            print("No new topics to add.")

        # --- Seed Resources ---
        existing_urls = {res.url for res in db.session.query(Resource.url).all()}
        resources_to_add = []
        for res_data in SAMPLE_RESOURCES:
            if res_data["url"] in existing_urls:
                print(f"  Skipping existing resource (URL): {res_data['title']}")
                continue

            # Find the corresponding Topic object
            topic = existing_topics.get(res_data["topic_name"])
            if not topic:
                print(f"  Warning: Topic '{res_data['topic_name']}' not found for resource '{res_data['title']}'. Skipping.")
                continue

            new_resource = Resource(
                title=res_data["title"],
                url=res_data["url"],
                resource_type=res_data["resource_type"], # Use Enum member
                difficulty=res_data["difficulty"],     # Use Enum member
                topic_id=topic.id # Assign the foreign key
                # 'topic' relationship attribute will be populated automatically via backref
            )
            resources_to_add.append(new_resource)
            existing_urls.add(res_data["url"]) # Add URL to set to prevent duplicates in this run
            print(f"  Preparing Resource: {res_data['title']} ({res_data['topic_name']})")

        if resources_to_add:
            db.session.add_all(resources_to_add)
            db.session.commit()
            print(f"Added {len(resources_to_add)} new resources.")
        else:
            print("No new resources to add.")

        print("Database seeding finished.")

if __name__ == '__main__':
    seed_database()
