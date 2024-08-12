# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    ingredients = db.Column(db.Text)
    instructions = db.Column(db.Text)
    category = db.Column(db.String(50))
