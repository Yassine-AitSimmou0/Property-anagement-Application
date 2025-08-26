# init_db.py
from app import app, db

with app.app_context():
    db.drop_all()
    db.create_all()
    print("Database initialized!")

# Run the script to initialize the database
# python init_db.py
# Output
# Database initialized!
# The script initializes the database by creating all the tables defined in the models.


