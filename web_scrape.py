import requests
from bs4 import BeautifulSoup
import sqlite3

def web_scraping():
    url = 'https://www.myjewishlearning.com/the-nosher/57-shabbat-dinner-recipes-youre-going-to-love/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    recipes = []
    for recipe in soup.find_all('article', class_='recipe-card'):
        title = recipe.find('h2').get_text().strip()
        ingredients = recipe.find('ul').get_text().strip().split('\n')
        instructions = recipe.find('div', class_='recipe-content').get_text().strip()
        category = section.get_text(strip=True)
        recipes.append((title, '\n'.join(ingredients), instructions, category))

    conn = sqlite3.connect('recipes.db')
    c = conn.cursor()

    c.executemany('INSERT INTO recipes (title, ingredients, instructions, category) VALUES (?, ?, ?, ?)', recipes)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    web_scraping()