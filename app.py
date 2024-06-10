'''import requests
import pandas as pd
from bs4 import BeautifulSoup'''

from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHMEY_DATABASE_URL'] ='sqlite:///' + os.path.join(basedir, 'db.sqlite')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    ingredients = db.Column(db.Text)
    instructions = db.Column(db.Text)
    category = db.Column(db.String(50))

@app.get("/")
def home():
    ingredient_list = db.session.query(Recipe).all()
    return render_template('base.html', recipes=recipes)

'''
# collecting our page from the website
page = "https://www.myjewishlearning.com/the-nosher/passover-recipes-carrot-kugel/"
soup = BeautifulSoup(requests.get(page).content, 'html.parser')
print(soup.find('h2').text.strip())

ingredients = []
for li in soup.select('tasty-recipes-entry-content'):
    ingred = ' '.join(li.text.split())
    ingredients.append(ingred)
print(ingredients)
# print(soup.prettify())  # printing each html tag on its own line

# filtering our url search to only get the urls that contain word recipe

recipe_urls = pd.Series([a.get("href") for a in soup.find_all("a")])
recipe_urls = recipe_urls[(recipe_urls.str.count("-")>0) &
(recipe_urls.str.contains("/recipes/")==True) &
(recipe_urls.str.contains("-recipes/")==True) & 
(recipe_urls.str.contains("course")==False) & 
(recipe_urls.str.contains("books")==False) & 
(recipe_urls.str.endswith("recipes/")==False)].unique()

df['recipe_urls'] = "https://www.myjewishlearning.com/the-nosher/57-shabbat-dinner-recipes-youre-going-to-love/" + df['recipe_urls'].astype('str')


recipe_name_list = soup.find(class_='m-content__body')  # our class

# finding all instances of <a> tag within class
recipe_name_list_items = recipe_name_list.find_all('a')
# printing out all the recipe names
for recipe_name in recipe_name_list_items:
    names = recipe_name.contents[0]
    links = 'https://www.myjewishlearning.com/the-nosher/57-shabbat-dinner-recipes-youre-going-to-love/' + recipe_name.get('href')
    print(names)
    print(links)

'''
