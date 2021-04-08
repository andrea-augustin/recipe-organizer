from difflib import SequenceMatcher
from string import punctuation, digits

path_frami = "../../data/resources/de_DE_frami.dic"

amount_types = [
    'g', 'kg', 'lb', 'ml', 'l', 'cups', 'cup', 'el', 'tl', 'ml', 'tbsp', 'tsp', 'msp', 'msp.', 'messerspitze', 'stiele',
    'stiel', 'zweige', 'zweig', 'dosen', 'dose', 'blatt', 'blätter', 'bund', 'cl', 'scheibe', 'scheiben', 'glas',
    'gläser', 'spritzer', 'stangen', 'prise', 'beutel', 'becher', 'tropfen', 'pk.', 'paket', 'pakete', 'würfel'
]


def compare_ingredients_with_frami_dict(path_all_ingredients, tagger):
    frami_dict = load_frami_dict_file()
    found_words = []

    with open(path_all_ingredients, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for line in lines:
        formatted_ingredient = format_ingredient_line(line)
        tagged_ingredient = tagger.tag_sent(formatted_ingredient)

        for element in tagged_ingredient:
            found_word = get_base_form_of_word(element, frami_dict)

            if found_word is not None and len(found_word) > 0 and found_word not in found_words:
                found_words.append(found_word)


def load_frami_dict_file():
    out = dict()
    with open(path_frami, 'r') as f:
        lines = f.readlines()

    for line in lines[18:]:
        line = line.replace('\n', '').split('/')

        if line[0][0] not in out:
            out[line[0][0]] = dict()

        if len(line) == 1:
            out[line[0][0]][line[0]] = ""
        else:
            out[line[0][0]][line[0]] = line[1]

    return out


def get_most_similar_word_from_frami_dict(word_to_check, frami_dict):
    words_with_same_starting_letter = frami_dict[word_to_check[0]].keys()
    best_score = 0
    most_similar_word = ""
    for word in words_with_same_starting_letter:
        score = SequenceMatcher(None, word_to_check, word).ratio()

        if score > best_score:
            best_score = score
            most_similar_word = word

    return most_similar_word


def get_base_form_of_word(tagged_word, frami_dict):
    if tagged_word[0][0] not in frami_dict:
        return ""

    if tagged_word[0] not in frami_dict[tagged_word[0][0]]:
        """
        if tagged_word[0] not in similarity_ingredient_dict:
            return get_most_similar_word_from_frami_dict(tagged_word[0], frami_dict)
        else:
            return tagged_word[0]
        """
        pass
    else:
        return tagged_word[0]


def format_ingredient_line(ingredient):
    formatted_ingredient = ingredient.rstrip('\n')
    formatted_ingredient = formatted_ingredient.translate(ingredient.maketrans('', '', punctuation))
    formatted_ingredient = formatted_ingredient.translate(formatted_ingredient.maketrans('', '', digits))
    formatted_ingredient = remove_amount_types(formatted_ingredient)

    return formatted_ingredient


def remove_amount_types(ingr):
    formatted_input = ingr.replace(u'\xa0', u' ').split(' ')
    out = []
    for element_in_formatted_input in formatted_input:
        if element_in_formatted_input.lower() in amount_types:
            continue

        if element_in_formatted_input == ' ':
            continue

        if 'à' in element_in_formatted_input:
            continue

        if len(element_in_formatted_input) == 0:
            continue

        out.append(element_in_formatted_input)
    return out
