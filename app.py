import requests
from bs4 import BeautifulSoup

# collecting our page from the website
page = requests.get("https://www.myjewishlearning.com/the-nosher/57-shabbat-dinner-recipes-youre-going-to-love/")
soup = BeautifulSoup(page.text, 'html.parser')
# print(soup.prettify())  # printing each html tag on its own line

recipe_name_list = soup.find(class_='m-content__body')  # our class

# finding all instances of <a> tag within class
recipe_name_list_items = recipe_name_list.find_all('a')
# printing out all the recipe names
for recipe_name in recipe_name_list_items:
    names = recipe_name.contents[0]
    links = 'https://www.myjewishlearning.com/the-nosher/57-shabbat-dinner-recipes-youre-going-to-love/' + recipe_name.get('href')
    print(names)
    print(links)

