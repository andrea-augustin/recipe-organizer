from time import sleep
import grabbers.utils

url_basic = "https://www.justonecookbook.com/"


def scrap_skipped_recipes(path_to_processed_recipes):
    with open('skipped.txt', 'r') as f:
        urls = f.readlines()

    recipes = []

    for url in urls:
        url = url.strip('\n')

        soup = grabbers.utils.create_soup_object(url)

        recipe = scrap_just_one_cookbook_recipe(soup, url)
        recipes.append(recipe)

        sleep(1)

    for recipe in recipes:
        grabbers.utils.save_recipe_to_file(recipe, path_to_processed_recipes)


def scrap_just_one_cookbook_page():
    for i in range(1, 58):
        recipe_links = []
        recipes = []
        skipped = []

        print("Seite " + str(i) + " von 57")

        url = url_basic + 'recipes/page/' + str(i) + '/'
        soup = grabbers.utils.create_soup_object(url)

        page_recipe_overview = soup.find("div", class_="recipes cr")
        for article in page_recipe_overview.find_all('article'):
            recipe_links.append(article.find("a")["href"])

        sleep(1)

        for recipe_url in recipe_links:
            soup_single_recipe_page = grabbers.utils.create_soup_object(recipe_url)

            try:
                recipe = scrap_just_one_cookbook_recipe(soup_single_recipe_page, recipe_url)
            except Exception:
                print("Seite übersprungen: " + recipe_url)
                skipped.append(recipe_url)
                sleep(1)
                continue

            if recipe is None:
                print("Seite kein Rezept: " + recipe_url)
                sleep(1)
                continue

            recipes.append(recipe)

        file_path = 'just_one_cookbook.txt'
        for recipe in recipes:
            grabbers.utils.save_recipe_to_file(recipe, file_path)

        if len(skipped) == 0:
            continue

        with open("skipped.txt", 'a', encoding="utf-8") as f:
            for skipped_recipe in skipped:
                f.write(skipped_recipe + '\n')

        sleep(1)


def get_ingredients_information_from_joc_recipe_page(soup):
    ingredients = []
    ingredients_elements = soup.find_all("div", class_="wprm-recipe-ingredient-group")

    for ing_container in ingredients_elements:
        if not ing_container.find("div", class_="wprm-recipe-group-name wprm-recipe-ingredient-group-name"):
            continue

        text = ing_container.find("div", class_="wprm-recipe-group-name wprm-recipe-ingredient-group-name").text

        if 'Optional' in text:
            for ing_element in ing_container.find_all("li"):
                ingredients.append(" ".join([ing.text for ing in ing_element.find_all("span")]) + " (Optional)")
            continue

        for ing_element in ing_container.find_all("li"):
            ingredients.append(" ".join([ing.text for ing in ing_element.find_all("span")]))

    return ingredients


def get_prep_steps_information_from_joc_recipe_page(soup):
    instructions = []
    instructions_element = soup.find("ol", class_="wprm-recipe-instructions")

    for inst_element in instructions_element.find_all("li"):
        instructions.append("\n".join([inst_element.text for inst_element in
                                       inst_element.find_all("div", class_="wprm-recipe-instruction-text")]))

    return instructions


def get_prep_time_information_from_joc_recipe_page(soup):
    prep_times = []
    prep_elements = soup.find_all('div', class_="wprm-recipe-time-container wprm-color-border")

    for prep in prep_elements:
        prep_times.append(' '.join([abc.text for abc in prep.find_all('span')]))

    return prep_times


def get_servings_information_from_joc_recipe_page(soup):
    servings_element = soup.find("div", class_="wprm-recipe-details-container").find("span",
                                                                                     class_="wprm-recipe-details-unit wprm-recipe-servings-unit")

    if servings_element is None:
        return 0
    else:
        return servings_element.text


def get_categories_information_from_joc_recipe_page(soup):
    return "\t".join(
        [single_type.text for single_type in soup.find("div", class_="post-cat col-3 middle").find_all("a")])


def get_recipe_title_information_from_joc_recipe_page(soup):
    return soup.find("div", class_="wprm-recipe-name wprm-color-header").text


def get_occasion_information_from_joc_recipe_page(soup):
    return soup.find("div", class_="wprm-recipe-details-container").find("span", class_="wprm-recipe-course").text


def check_if_joc_page_is_a_recipe_page(soup):
    if soup.find("div", class_="wprm-recipe-ingredient-group") is None:
        return False

    if soup.find("div", class_="wprm-recipe-details-container") is None:
        return False

    if soup.find("ol", class_="wprm-recipe-instructions") is None:
        return False

    return True


def scrap_just_one_cookbook_recipe(soup, recipe_url):
    # TODO relegate into function
    if not check_if_joc_page_is_a_recipe_page(soup):
        return None

    recipe = dict()

    recipe['url'] = recipe_url
    recipe['title'] = get_recipe_title_information_from_joc_recipe_page(soup)
    recipe['categories'] = get_categories_information_from_joc_recipe_page(soup)
    recipe['occasion'] = get_occasion_information_from_joc_recipe_page(soup)
    recipe['servings'] = get_prep_time_information_from_joc_recipe_page(soup)
    recipe['ingredients'] = get_ingredients_information_from_joc_recipe_page(soup)
    recipe['steps'] = get_prep_steps_information_from_joc_recipe_page(soup)
    recipe['prep_time'] = get_prep_time_information_from_joc_recipe_page(soup)

    return recipe


if __name__ == '__main__':
    pass
