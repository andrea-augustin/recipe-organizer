import os
from string import punctuation

from old_code import parser_grammar, utils

"""
file with different approaches to parse ingredients but did not work as hoped
"""

ingredient_list = []


class lineParserIngredientElement:
    def __init__(self):
        self.ingredient_name = ""
        self.amount = 0
        self.amount_type = ""
        self.ingredient_additional_info = []

        self.current_pos = 0

    def set_ingredient_name(self, name):
        self.ingredient_name = name

    def set_amount(self, amount):
        self.amount = amount

    def set_amount_type(self, amount_type):
        self.amount_type = amount_type

    def extend_ingredient_additional_info(self, new_info):
        self.ingredient_additional_info.append(new_info)

    def line_parser_parse_amount(self, ingredient_line):
        new_pos = self.current_pos
        string_amount = ""

        while ingredient_line[new_pos].isdigit() or ingredient_line[new_pos] in ('.', ','):
            if ingredient_line[new_pos] == ',':
                string_amount += '.'
                new_pos += 1
                continue

            string_amount += ingredient_line[new_pos]
            new_pos += 1

        if len(string_amount) == 0:
            self.set_amount(0)
            self.current_pos = new_pos
        else:
            self.set_amount(float(string_amount))
            self.current_pos = new_pos

    def line_parser_parse_amount_type(self, ingredient_line):
        new_pos = self.current_pos + 1 if ingredient_line[self.current_pos].isspace() else self.current_pos
        string_amount_type = ""

        while new_pos < len(ingredient_line) and not ingredient_line[new_pos].isspace():
            string_amount_type += ingredient_line[new_pos]
            new_pos += 1

        string_amount_type = string_amount_type.lower()

        if string_amount_type in parser_grammar.grammar[parser_grammar.grammar_amount_type]:
            self.set_amount_type(string_amount_type)
            self.current_pos = new_pos
        else:
            self.set_amount_type("")
            self.current_pos = self.current_pos

    def line_parser_parse_ingredient_name(self, ingredient_line):
        if len(ingredient_line) == self.current_pos:
            print('Ingredient could not be read properly:\n', ingredient_line)
            self.set_ingredient_name("")
            return

        new_pos = self.current_pos + 1 if ingredient_line[self.current_pos].isspace() else self.current_pos
        string_ingredient_name = ""
        while new_pos < len(ingredient_line) and \
                (ingredient_line[new_pos].isspace() or ingredient_line[new_pos].isalnum() or ingredient_line[
                    new_pos] == '.'):
            string_ingredient_name += ingredient_line[new_pos]
            new_pos += 1

        if len(string_ingredient_name) == 0:
            self.current_pos = new_pos
            self.line_parser_parse_additional_info(ingredient_line)
            self.line_parser_parse_ingredient_name(ingredient_line)
        else:
            if string_ingredient_name[-1].isspace():
                string_ingredient_name = string_ingredient_name.rstrip()

            self.set_ingredient_name(string_ingredient_name)

        self.current_pos = new_pos

    def line_parser_parse_additional_info(self, ingredient_line):
        new_pos = self.current_pos
        string_additional_info = ""

        if ingredient_line[new_pos] == '(':
            new_pos += 1
            while new_pos < len(ingredient_line) and ingredient_line[new_pos] != ')':
                string_additional_info += ingredient_line[new_pos]
                new_pos += 1
            new_pos += 1
        else:
            while new_pos < len(ingredient_line) and not ingredient_line[new_pos].isalnum():
                new_pos += 1

            if new_pos == len(ingredient_line):
                self.current_pos = new_pos
                return

            while new_pos < len(ingredient_line):
                if ingredient_line[new_pos] not in [',', '.', '(', ')', ';']:
                    string_additional_info += ingredient_line[new_pos]

                if ingredient_line[new_pos] == ',' and ingredient_line[new_pos - 1].isalnum() and ingredient_line[
                    new_pos + 1].isalnum():
                    string_additional_info += ingredient_line[new_pos]

                new_pos += 1

        self.extend_ingredient_additional_info(string_additional_info)
        self.current_pos = new_pos

    def parse_ingredients_line_parser(self, ingredient):
        values_to_check = [
            'geschrotete, getrocknete Chilischote'
        ]

        for word in ingredient.split(' '):
            if not word.isalpha():
                continue
            if word in parser_grammar.grammar[parser_grammar.grammar_amount_type]:
                continue

        self.line_parser_parse_amount(ingredient)
        self.line_parser_parse_amount_type(ingredient)
        self.line_parser_parse_ingredient_name(ingredient)
        if self.current_pos < len(ingredient):
            self.line_parser_parse_additional_info(ingredient)

        if self.ingredient_name[0].islower():
            temp_name = self.ingredient_name.split(' ')

            while len(temp_name) > 1 and (temp_name[0][0].islower() or temp_name[0].lower() in parser_grammar.grammar[
                parser_grammar.grammar_amount_type]):
                if temp_name[0][0].islower():
                    self.ingredient_additional_info.append(temp_name[0])
                    temp_name.pop(0)

                if temp_name[0].lower() in parser_grammar.grammar[parser_grammar.grammar_amount_type]:
                    self.amount_type = temp_name[0].lower()
                    temp_name.pop(0)

            self.ingredient_name = ' '.join(temp_name)

        if len(self.ingredient_name.split(' ')) == 1:
            return [self.ingredient_name]
        else:
            return []


def parser_main(filename_single_ingredients_list, directory, path_all_ingredients):
    differences_ingredients = set()
    with open(filename_single_ingredients_list, 'r', encoding='utf-8') as f:
        set_ingredients_from_file = set(f.read().splitlines())

    for filename in os.listdir(directory):
        set_new_ingredients = utils.read_recipe_file(os.path.join(directory, filename))
        differences_ingredients = differences_ingredients.union(
            set_ingredients_from_file.symmetric_difference(set_new_ingredients))

    with open(path_all_ingredients, 'w', encoding='utf-8') as f:
        for item in ingredient_list:
            f.write("%s\n" % item)


def main(path_to_ingredients_list):
    name_ingr_list = set()
    amount_name_ingr_list = []
    amount_type_ingr_list = []
    others_list = []

    with open(path_to_ingredients_list, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for line in lines:
        formatted_line = line.rstrip('\n')
        formatted_line = formatted_line.translate(formatted_line.maketrans(punctuation, ' ' * len(punctuation)))
        formatted_line = formatted_line.replace('\xa0', '')
        split_line = formatted_line.split(' ')

        if len(split_line) == 1 and split_line[0].isalpha():
            name_ingr_list.add(split_line[0])
        elif len(split_line) == 2 and (split_line[0].isdigit() or '.' in split_line[0]) and split_line[1].isalpha():
            amount_name_ingr_list.append(' '.join(split_line))
        elif len(split_line) == 3 and (split_line[0].isdigit() or '.' in split_line[0]) and split_line[1].lower() in \
                parser_grammar.grammar[parser_grammar.grammar_amount_type] and split_line[2].isalpha():
            amount_type_ingr_list.append(' '.join(split_line))
        else:
            others_list.append(' '.join(split_line))

    ingredient_set = name_ingr_list.copy()

    for i in range(len(amount_name_ingr_list) - 1, -1, -1):
        if amount_name_ingr_list[i][0] == '1':
            amount, name = amount_name_ingr_list[i].split(' ')
            if name in ingredient_set:
                continue
            else:
                ingredient_set.add(name)

    test = sorted(list(name_ingr_list))
    print(1231)
