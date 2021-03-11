from bs4 import BeautifulSoup
import requests
from os.path import exists


def save_recipe_to_file(recipe, path):
    file_open_mode = 'a' if exists(path) else 'w'

    with open(path, file_open_mode, encoding='utf-8') as f:
        f.write("Titel\t" + recipe['title'] + "\n")
        f.write("URL\t" + recipe['url'] + "\n")
        f.write("Seite\t" + str(recipe['page']) + "\n")
        f.write("Portionen\t" + str(recipe['servings']) + "\n")
        f.write("Dauer\t" + recipe['prep_time'] + "\n")
        if recipe['categories'] is None:
            f.write("Kategorien\n")
        else:
            f.write("Kategorien\t" + '\t'.join(recipe['categories']) + "\n")
        f.write("Zutaten\n")
        for ingredient in recipe['ingredients']:
            f.write(ingredient + "\n")
        f.write("Zubereitung\n")
        for step in recipe['steps']:
            f.write(step + "\n")
        f.write("\n")


def create_soup_object(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')

    return soup
