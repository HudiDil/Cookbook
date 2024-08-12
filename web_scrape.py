import requests
from bs4 import BeautifulSoup
import sqlite3

def web_scraping():
    url = 'https://www.myjewishlearning.com/the-nosher/57-shabbat-dinner-recipes-youre-going-to-love/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    recipes = []

    for section in soup.find_all('section', class_='m-detail--body'):
        if category_header:
            category = category_header.get_text(strip=True)

        for recipe in section.find_all('div', class_='tasty-recipes'):
            title = recipe.find('h2', class_='entry-title').get_text().strip()

            ingredients_list = recipe.find('div', class_='tasty-recipes-ingredients')
            if ingredients_list:
                ingredients = ingredients_list.get_text(separator='\n').strip()

            instructions_div = recipe.find('div', class_='tasty-recipes-instructions')
            if instructions_div:
                instructions = instructions_div.get_text(separator='\n').strip()

            recipes.append((title, ingredients, instructions, category))

    conn = sqlite3.connect('recipes.db')
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            ingredients TEXT,
            instructions TEXT,
            category TEXT
        )
    ''')

    c.executemany('INSERT INTO recipes (title, ingredients, instructions, category) VALUES (?, ?, ?, ?)', recipes)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    web_scraping()
