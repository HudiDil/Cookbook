from flask import Flask, render_template, request, redirect, url_for
from models import db, Recipe
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def home():
    recipes = Recipe.query.all()
    return render_template('base.html', recipes=recipes)

@app.route('/add', methods=['GET', 'POST'])
def add_recipe():
    if request.method == 'POST':
        title = request.form['title']
        ingredients = request.form['ingredients']
        instructions = request.form['instructions']
        category = request.form.get('category', 'Unknown')
        
        if title:
            new_recipe = Recipe(title=title, ingredients=ingredients, instructions=instructions, category=category)
            db.session.add(new_recipe)
            db.session.commit()
            return redirect(url_for('home'))
    
    return render_template('add.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    if query:
        recipes = Recipe.query.filter((Recipe.title.ilike(f'%{query}%')) | (Recipe.ingredients.ilike(f'%{query}%'))).all()
    else:
        recipes = []
    return render_template('search.html', recipes=recipes, query=query)

@app.route('/category/<category_name>')
def category(category_name):
    recipes = Recipe.query.filter_by(category=category_name).all()
    return render_template('category.html', recipes=recipes, category_name=category_name)

if __name__ == '__main__':
    app.run(debug=True)
