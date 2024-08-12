import requests
from bs4 import BeautifulSoup
from app import app, db, Recipe

def scrape_recipes():
    with app.app_context():
        url = 'https://www.myjewishlearning.com/the-nosher/57-shabbat-dinner-recipes-youre-going-to-love/'
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        recipes = []
        for recipe in soup.find_all('article', class_='recipe-card'):
            title = recipe.find('h2').get_text().strip()
            ingredients_list = recipe.find('ul')
            ingredients = '\n'.join([item.get_text().strip() for item in ingredients_list.find_all('li')]) if ingredients_list else 'No ingredients listed'
            instructions = recipe.find('div', class_='recipe-content').get_text().strip() if recipe.find('div', class_='recipe-content') else 'No instructions listed'
            category = 'Unknown'  # Adjust this if you have a way to determine the category

            recipes.append((title, ingredients, instructions, category))

        # Insert into the database
        for title, ingredients, instructions, category in recipes:
            new_recipe = Recipe(title=title, ingredients=ingredients, instructions=instructions, category=category)
            db.session.add(new_recipe)
        db.session.commit()
        print(f"{len(recipes)} recipes have been scraped and added to the database.")

if __name__ == "__main__":
    scrape_recipes()
