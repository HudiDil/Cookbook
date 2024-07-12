from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
DATABASE = 'recipes.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_db():
    connection = get_db_connection()
    with open('schema.sql') as f:
        connection.executescript(f.read())
    connection.close()

def create_collections():
    collections = [
        "Soups, Sides and Starters",
        "Main dishes - Chicken",
        "Main dishes - Fish",
        "Main dishes - Beef",
        "Desserts"
    ]
    conn = get_db_connection()
    for collection in collections:
        conn.execute('INSERT OR IGNORE INTO collections (name) VALUES (?)', (collection,))
    conn.commit()
    conn.close()

def scrape_recipes():
    url = "https://www.myjewishlearning.com/the-nosher/57-shabbat-dinner-recipes-youre-going-to-love/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    sections = soup.select('h3, h2')
    recipes = []
    for section in sections:
        category = section.get_text(strip=True)
        collection_id = None
        conn = get_db_connection()
        collection = conn.execute('SELECT id FROM collections WHERE name = ?', (category,)).fetchone()
        if collection:
            collection_id = collection['id']
        conn.close()

        next_element = section.find_next()
        while next_element and next_element.name not in ['h3', 'h2']:
            if next_element.name == 'a':
                recipe_name = next_element.get_text(strip=True)
                recipe_link = next_element['href']
                recipes.append((recipe_name, recipe_link, collection_id))
            next_element = next_element.find_next()

    conn = get_db_connection()
    for recipe in recipes:
        conn.execute(
            'INSERT INTO recipes (name, ingredients, instructions, collection_id) VALUES (?, ?, ?, ?)',
            (recipe[0], recipe[1], '', recipe[2])
        )
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = get_db_connection()
    collections = conn.execute('SELECT * FROM collections').fetchall()
    conn.close()
    return render_template('index.html', collections=collections)

@app.route('/add', methods=('GET', 'POST'))
def add_recipe():
    conn = get_db_connection()
    collections = conn.execute('SELECT * FROM collections').fetchall()
    conn.close()
    if request.method == 'POST':
        name = request.form['name']
        ingredients = request.form['ingredients']
        instructions = request.form['instructions']
        collection_id = request.form['collection_id']
        
        conn = get_db_connection()
        conn.execute(
            'INSERT INTO recipes (name, ingredients, instructions, collection_id) VALUES (?, ?, ?, ?)',
            (name, ingredients, instructions, collection_id)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add.html', collections=collections)

@app.route('/search', methods=('GET', 'POST'))
def search():
    recipes = []
    if request.method == 'POST':
        query = request.form['query']
        conn = get_db_connection()
        recipes = conn.execute(
            "SELECT * FROM recipes WHERE name LIKE ? OR ingredients LIKE ?",
            ('%' + query + '%', '%' + query + '%')
        ).fetchall()
        conn.close()
    return render_template('search.html', recipes=recipes)

@app.route('/recipe/<int:recipe_id>')
def recipe(recipe_id):
    conn = get_db_connection()
    recipe = conn.execute('SELECT * FROM recipes WHERE id = ?', (recipe_id,)).fetchone()
    conn.close()
    return render_template('recipe.html', recipe=recipe)

if __name__ == '__main__':
    initialize_db()
    create_collections()
    scrape_recipes()
    app.run(host="0.0.0.0", debug=True)
