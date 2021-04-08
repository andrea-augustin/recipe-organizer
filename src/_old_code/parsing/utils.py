import os


def read_recipe_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content_of_file = f.read()

    recipes_file = content_of_file.split('\n\n')

    return recipes_file


def fix_encoding_in_files(directory):
    for filename in os.listdir(directory):
        with open(os.path.join(directory, filename), 'r', encoding='utf-8') as f:
            lines = f.readlines()

        with open(os.path.join(directory, filename), 'w', encoding='utf-8') as out:
            for line in lines:
                test = [i for i, ltr in enumerate(line) if ltr == '̈']

                if len(test) == 0:
                    out.write(line)
                    continue

                for wrong_letter in reversed(test):
                    correct_letter = get_correct_umlaut_letter(line, wrong_letter)
                    line = line[:wrong_letter - 1] + correct_letter + line[wrong_letter + 1:]
                out.write(line)


def get_correct_umlaut_letter(text, idx):
    if text[idx - 1] == 'u':
        return 'ü'
    elif text[idx - 1] == 'U':
        return 'Ü'
    elif text[idx - 1] == 'a':
        return 'ä'
    elif text[idx - 1] == 'A':
        return 'Ä'
    elif text[idx - 1] == 'o':
        return 'ö'
    elif text[idx - 1] == 'Ö':
        return 'Ö'
    else:
        return ''


def fix_ingredient_typos_in_files(names, directory, path_all_recipes):
    complete_file = open(path_all_recipes, 'w', encoding='utf-8')

    for filename in os.listdir(directory):
        with open(os.path.join(directory, filename), 'r', encoding='utf-8') as f:
            lines = f.readlines()

        with open(os.path.join(directory, filename), 'w', encoding='utf-8') as out:
            for line in lines:
                new_line = replace_wrong_ingredient_name(names, line)
                out.write(new_line)
                complete_file.write(new_line)

    complete_file.close()


def save_categories_to_file(directory, path_categories):
    categories_list = []
    for filename in os.listdir(directory):
        path = os.path.join(directory, filename)

        with open(path, 'r', encoding='utf-8') as f:
            file_content = f.read()

        recipes_file = file_content.split('\n\n')

        for recipe_file in recipes_file:
            if len(recipe_file) == 0:
                break

            recipe_file = recipe_file.split('\n')
            categories_list += recipe_file[5].split('\t')[1:]

    categories_set = set(categories_list)
    with open(path_categories, 'w', encoding='utf-8') as f:
        for item in categories_set:
            f.write("%s\n" % item)


def replace_wrong_ingredient_name(dict_names, line):
    for name in dict_names:
        if name in line:
            return line.replace(name, dict_names[name])
    return line
