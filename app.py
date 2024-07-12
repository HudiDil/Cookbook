from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DATABASE = 'recipes.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    recipes = conn.execute('SELECT * FROM recipes').fetchall()
    conn.close()
    return render_template('index.html', recipes=recipes)

@app.route('/add', methods=['GET', 'POST'])
def add_recipe():
    if request.method == 'POST':
        title = request.form['title']
        ingredients = request.form['ingredients']
        instructions = request.form['instructions']
        category = request.form['category']

        conn = get_db_connection()
        conn.execute('INSERT INTO recipes (title, ingredients, instructions, category) VALUES (?, ?, ?, ?)',
                     (title, ingredients, instructions, category))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add.html')

# Search page
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form['query']
        conn = get_db_connection()
        # Fetch recipes matching the query and include category
        results = conn.execute('SELECT title, ingredients, instructions, category FROM recipes WHERE title LIKE ? OR ingredients LIKE ?',
                               ('%' + query + '%', '%' + query + '%')).fetchall()
        conn.close()
        return render_template('search_results.html', results=results, query=query)
    return render_template('search.html')


if __name__ == '__main__':
    app.run(debug=True)

