import requests
from bs4 import BeautifulSoup
from app import app, db
from models import Recipe
from urllib.parse import urljoin

def fetch_recipe_details(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')

    ingredients_div = soup.find('div', class_='m-content__recipe--ingredients')
    instructions_div = soup.find('div', class_='m-content__recipe--directions')

    ingredients = ingredients_div.get_text(strip=True, separator='\n')
    instructions = instructions_div.get_text(strip=True, separator='\n')
    
    return ingredients, instructions

def scrape_recipes():
    with app.app_context():
        base_url = 'https://www.myjewishlearning.com/the-nosher/57-shabbat-dinner-recipes-youre-going-to-love/'
        response = requests.get(base_url)
          
        soup = BeautifulSoup(response.content, 'html.parser')
        recipes = []
        recipe_links = soup.find_all('a', href=True)
        
        for link in recipe_links:
            href = link.get('href')
            title = link.get_text(strip=True)
            if not href.startswith('https://www.myjewishlearning.com/recipe/') or not title:
                continue

            full_url = urljoin(base_url, href)

            if full_url.startswith('http'):
                ingredients, instructions = fetch_recipe_details(full_url)

                if 'appetizer' in title.lower():
                    category = 'appetizers'
                elif 'main' in title.lower():
                    category = 'mains'
                elif 'dessert' in title.lower():
                    category = 'desserts'
                else:
                    category = 'unknown'

                recipes.append((title, ingredients, instructions, category))

        if recipes:
            for title, ingredients, instructions, category in recipes:
                new_recipe = Recipe(title=title, ingredients=ingredients, instructions=instructions, category=category)
                db.session.add(new_recipe)
            db.session.commit()
            print(f"{len(recipes)} recipes have been scraped correctly to the database.")
        else:
            print("Sorry. Web scraping didn't work well.")

if __name__ == "__main__":
    scrape_recipes()
