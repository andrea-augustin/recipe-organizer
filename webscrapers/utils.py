from bs4 import BeautifulSoup
import copy
import requests
import os.path
import json


def unify_scraped_recipes_with_recipes_from_json_file(scraped_recipes, recipes_from_json):
    updated_recipes = copy.deepcopy(recipes_from_json)

    for recipe in scraped_recipes['recipes']:
        if recipe in recipes_from_json:
            continue

        updated_recipes['recipes'].extend(recipe)

    return updated_recipes


def save_recipes_to_json_file(recipes, path):
    recipes_to_save = recipes

    if os.path.exists(path):
        with open(path, encoding='utf-8') as json_file:
            recipes_from_file = json.load(json_file)

        recipes_to_save = unify_scraped_recipes_with_recipes_from_json_file(recipes, recipes_from_file)

    with open(path, 'w', encoding='utf-8') as out:
        json.dump(recipes_to_save, out, indent=4, ensure_ascii=False)


def save_skipped_recipes_to_txt_file(list_of_urls, path):
    with open(path, 'a', encoding="utf-8") as f:
        for skipped_recipe_url in list_of_urls:
            f.write(skipped_recipe_url + '\n')

def save_recipe_to_txt_file(recipe, path):
    file_open_mode = 'a' if os.path.exists(path) else 'w'

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
        f.write("Zutaten\t" + '\t'.join(recipe['ingredients']) + '\n')
        f.write("Zubereitung\t" + '\t'.join(recipe['steps']) + '\n')
        f.write("\n")


def create_soup_object(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')

    return soup
