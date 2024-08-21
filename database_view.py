from app import app, db  # Directly import app and db
from models import User  # Import your models

# Create a context to run database queries
with app.app_context():
    users = User.query.all()

    for user in users:
        print(f"ID: {user.id}, Username: {user.username}, Name: {user.name}, Email: {user.email}, Bio: {user.bio}, Image File: {user.image_file}")


# from app import app, db  # Directly import app and db
# from models import Brief  # Import your models

# # Create a context to run database queries
# with app.app_context():
#     users = Brief.query.all()

#     for user in users:
#         print(f"ID: {user.id}, type: {user.type}, Domain: {user.domain}, Content: {user.content}, date_posted: {user.date_posted}, userid: {user.user_id}")



# from app import app, db  # Directly import app and db
# from models import BriefHistory  # Import your models

# # Create a context to run database queries
# with app.app_context():
#     users = BriefHistory.query.all()

#     for user in users:
#         print(f"ID: {user.id}, userid: {user.user_id}, type: {user.brief_type}, domain: {user.domain}, generated brief: {user.generated_brief}, time: {user.timestamp}")


