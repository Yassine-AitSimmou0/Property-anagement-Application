from source.auth.models import User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from source.database import db  # Adjust this import according to your project structure
from werkzeug.security import generate_password_hash

# Create a new SQLAlchemy engine and session
DATABASE_URL = "postgresql+psycopg2://username:password@db:5432/property_management_db"  # Update with your database URL
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

def generate_random_users():
    users_data = [
        {
            'name': "admin",
            'email': "admin@test.com",
            'password': generate_password_hash("adminadmin"),
        },
        
    ]
    users = []
    for user in users_data:
        user_instance = User(**user)
        users.append(user_instance)
    return users


def main():
    # Generate and add users
    try: 
        users = generate_random_users()
        session.add_all(users)
        session.commit()
        print("Users added successfully!")
    except Exception:
        print(f"User Already Exists !!")

if __name__ == "__main__":
    main()
