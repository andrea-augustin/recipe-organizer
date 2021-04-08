from tkinter import filedialog
import json
import re


def replace_xa0_with_whitespace(input_text):
    return input_text.replace(u'\xa0', u' ')


def replace_xad_with_minus(input_text):
    return input_text.replace(u'\xad', u'-')


def fix_unicode_characters_text(text):
    if u'\xa0' in text:
        out = replace_xa0_with_whitespace(text)
    elif u'\xad' in text:
        out = replace_xad_with_minus(text)
    else:
        return text

    return out


def read_recipe_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content_of_file = f.read()

    recipes_from_file = content_of_file.split('\n\n')

    return recipes_from_file


def get_specific_list_idx_from_single_recipe(recipe, string_to_search):
    r = re.compile(string_to_search)
    elements_found = list(filter(r.match, recipe))

    if len(elements_found) == 0:
        return -1

    return recipe.index(elements_found[0])


def get_title_of_recipe_from_text_file(recipe):
    title_idx = get_specific_list_idx_from_single_recipe(recipe, "^Titel")
    return recipe[title_idx].split('\t')[1]


def get_url_of_recipe_from_text_file(recipe):
    url_idx = get_specific_list_idx_from_single_recipe(recipe, "^URL")
    return recipe[url_idx].split('\t')[1]


def get_page_of_recipe_from_text_file(recipe):
    page_idx = get_specific_list_idx_from_single_recipe(recipe, "^Seite")

    if page_idx == -1:
        return -1
    else:
        return recipe[page_idx].split('\t')[1]


def get_servings_of_recipe_from_text_file(recipe):
    servings_idx = get_specific_list_idx_from_single_recipe(recipe, "^Portionen")
    return recipe[servings_idx].split('\t')[1]


def get_prep_time_of_recipe_from_text_file(recipe):
    prep_time_idx = get_specific_list_idx_from_single_recipe(recipe, "^Dauer")
    return recipe[prep_time_idx].split('\t')[1]


def get_categories_of_recipe_from_text_file(recipe):
    categories_idx = get_specific_list_idx_from_single_recipe(recipe, "^Kategorien")
    return recipe[categories_idx].split('\t')[1]


def prepare_recipe_for_json_format(recipe):
    idx_ingredients = recipe.index('Zutaten')
    idx_steps = recipe.index('Zubereitung')

    title = get_title_of_recipe_from_text_file(recipe)
    url = get_url_of_recipe_from_text_file(recipe)
    page = get_page_of_recipe_from_text_file(recipe)
    servings = get_servings_of_recipe_from_text_file(recipe)
    prep_time = get_prep_time_of_recipe_from_text_file(recipe)
    categories = get_categories_of_recipe_from_text_file(recipe)
    ingredients = recipe[idx_ingredients + 1:idx_steps]
    steps = recipe[idx_steps + 1:]

    out = {
        'title': title,
        'url': url,
        'page': page,
        'servings': servings,
        'prep_time': prep_time,
        'categories': categories,
        'ingredients': ingredients,
        'steps': steps
    }

    return out


def convert_text_file_to_json_file(path_to_text_file, path_to_json_file):
    with open(path_to_text_file, encoding='utf-8', mode='r') as f:
        text_file = f.read()

    text_file_split_into_recipes = text_file.split('\n\n')

    recipes_for_json_file = dict()
    recipes_for_json_file['recipes'] = []

    for single_recipe in text_file_split_into_recipes:
        if single_recipe == '':
            continue

        single_recipe_fixed_encoding = fix_unicode_characters_text(single_recipe)
        single_recipe_as_list = single_recipe_fixed_encoding.split('\n')

        formatted_recipe = prepare_recipe_for_json_format(single_recipe_as_list)

        recipes_for_json_file['recipes'].append(formatted_recipe)

    with open(path_to_json_file, 'w', encoding='utf-8') as out:
        json.dump(recipes_for_json_file, out, indent=4, ensure_ascii=False)


def main():
    convert_text_file_to_json_file(filedialog.askopenfilename(), 'converted_file.json')


if __name__ == '__main__':
    main()
