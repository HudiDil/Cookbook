from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'recipes.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the Recipe model
class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50))

@app.route("/")
def index():
    recipes = Recipe.query.all()
    return render_template('index.html', recipes=recipes)

@app.route("/add", methods=['GET', 'POST'])
def add_recipe():
    if request.method == 'POST':
        title = request.form['title']
        ingredients = request.form['ingredients']
        instructions = request.form['instructions']
        category = request.form['category']
        
        new_recipe = Recipe(title=title, ingredients=ingredients, instructions=instructions, category=category)
        db.session.add(new_recipe)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('add_recipe.html')

@app.route("/search", methods=['GET'])
def search():
    query = request.args.get('query')
    recipes = Recipe.query.filter(
        (Recipe.title.contains(query)) | (Recipe.ingredients.contains(query))
    ).all()
    return render_template('search_results.html', recipes=recipes, query=query)

if __name__ == '__main__':
    app.run(debug=True)
