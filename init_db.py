# init_db.py
from app import app
from models import db

def initialize_database():
    with app.app_context():
        db.create_all()
        print("Database has been initalized")

if __name__ == "__main__":
    initialize_database()
