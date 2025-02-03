from app.services.user import User
from app.services.database import Database

# Initialize the Database object
db = Database()

# Create a new user object
user = User("testuser", "password123")

# Register the user
try:
    result = user.register_user(db)
    print(result)
except ValueError as e:
    print(f"Registration Error: {e}")

# Authenticate the user
try:
    result = user.authenticate(db, "password123")
    print(result)
except ValueError as e:
    print(f"Authentication Error: {e}")
