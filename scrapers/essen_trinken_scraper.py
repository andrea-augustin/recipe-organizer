from time import sleep
import re
import scrapers.utils

url_basic = "https://www.essen-und-trinken.de"
url_archive = "https://www.essen-und-trinken.de/rezepte/archiv"


def scrap_skipped_eut_pages(path):
    with open(path, 'r') as f:
        urls = f.readlines()

    skipped = []

    for recipe_url in urls:
        recipe_url = recipe_url.strip('\n')

        soup_recipe = scrapers.utils.create_soup_object(recipe_url)
        recipe = scrap_essen_und_trinken_recipe(soup_recipe, recipe_url)

        if all(['essen_und_trinken' not in recipe['origin'], 'Für_jeden_Tag' not in recipe['origin'],
                'essen_und_trinken' not in recipe['origin']]):
            continue

        file_path = 'essen_und_trinken/' + recipe['origin'] + '.txt'

        scrapers.utils.save_recipe_to_file(recipe, file_path)

        sleep(1)

    if len(skipped) == 0:
        return

    with open("skipped.txt", 'a', encoding="utf-8") as f:
        for skipped_recipe in skipped:
            f.write(skipped_recipe + '\n')


def scrap_essen_und_trinken_pages():
    skipped = []

    for i in range(0, 1145):
        recipe_links = []

        print("Seite " + str(i + 1) + " von 1145")

        url = url_archive + '?page=' + str(i)
        soup = scrapers.utils.create_soup_object(url)

        page_recipe_overview = soup.find("div", class_="panel-panel panel-col")

        for a_element in page_recipe_overview.find_all('a', href=True):
            if 'rzpt' in a_element['href']:
                recipe_links.append(a_element['href'])

        sleep(1.5)

        for recipe_url in recipe_links:
            soup_single_recipe_page = scrapers.utils.create_soup_object(url_basic + recipe_url)

            try:
                recipe = scrap_essen_und_trinken_recipe(soup_single_recipe_page, url_basic + recipe_url)
            except Exception:
                print("Rezept übersprungen: " + url_basic + recipe_url)

                skipped.append(url_basic + recipe_url)
                sleep(1.5)

                continue

            if all(['essen_und_trinken' not in recipe['origin'], 'Für_jeden_Tag' not in recipe['origin'],
                    'essen_und_trinken' not in recipe['origin']]):
                continue

            file_path = recipe['origin'] + '.txt'

            scrapers.utils.save_recipe_to_file(recipe, file_path)

            sleep(1.5)

    if len(skipped) > 0:
        with open("skipped.txt", 'a', encoding="utf-8") as f:
            for skipped_recipe in skipped:
                f.write(skipped_recipe + '\n')


def get_origin_information_from_eut_recipe_page(soup):
    origin_element = soup.find("div", class_="recipe-references").find("div", class_="source-reference")

    if origin_element:
        return origin_element.text.split('\n')[-1].strip(' ').replace(' ', '_').replace('/', '_')
    else:
        return "essen_und_trinken"


def get_servings_information_from_eut_recipe_page(soup, ingredients_element):
    servings_element = soup.find("div", class_="servings")

    if servings_element:
        return servings_element.text.strip()
    else:
        specific_serving_elements = ingredients_element.find("ul", class_="ingredients-list").find_all("li",
                                                                                                       class_="ingredients-zwiti")

        if len(specific_serving_elements) == 0:
            return 0
        else:
            return specific_serving_elements[0].text


def get_prep_time_information_from_eut_recipe_page(soup):
    prep_time_element = soup.find("div", class_="time-preparation")

    if prep_time_element:
        prep_time = soup.find("div", class_="time-preparation").text
        additional_prep_element = soup.find_all("div", class_="time-addon")

        if additional_prep_element:
            for additional_prep in additional_prep_element:
                prep_time += ' ' + additional_prep.text

        return prep_time
    else:
        return "Nicht angegeben"


def get_categories_information_from_eut_recipe_page(soup):
    category_page_element = soup.find("ul", class_="taxonomies-list")

    if category_page_element is None:
        return None
    else:
        categories_children = category_page_element.findChildren('li', recursive=False)
        categories = []

        for category_element in categories_children:
            categories.append(category_element.text)

        return categories


def get_ingredients_information_from_eut_recipe_page(ingredients_element):
    ingredients = []
    for ingredient_element in ingredients_element.find_all('li'):
        if len(ingredient_element.attrs) > 0:
            continue

        ingredients.append(re.sub(' +', ' ', ingredient_element.text.strip()))

    return ingredients


def get_prep_steps_information_from_eut_recipe_page(soup):
    prep_steps = []
    prep_steps_element = soup.find("ul", class_="preparation").findChildren("li", class_="preparation-step",
                                                                            recursive=False)

    for step in prep_steps_element:
        prep_steps.append(step.find("div", class_="preparation-text").text)

    return prep_steps


def scrap_essen_und_trinken_recipe(soup, recipe_url):
    ingredients_element = soup.find("section", class_="ingredients")
    recipe = dict()

    recipe['url'] = recipe_url

    recipe['title'] = soup.find("span", class_="headline-title").text

    recipe['origin'] = get_origin_information_from_eut_recipe_page(soup)

    recipe['page'] = 0

    recipe['servings'] = get_servings_information_from_eut_recipe_page(soup, ingredients_element)

    recipe['prep_time'] = get_prep_time_information_from_eut_recipe_page(soup)

    recipe['categories'] = get_categories_information_from_eut_recipe_page(soup)

    recipe['ingredients'] = get_ingredients_information_from_eut_recipe_page(ingredients_element)

    recipe['steps'] = get_prep_steps_information_from_eut_recipe_page(soup)

    return recipe


if __name__ == '__main__':
    scrap_essen_und_trinken_pages()
