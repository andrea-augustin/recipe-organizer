import re
from operator import itemgetter

regex_rules = [
    r'(\d+\s\w+)(\s(\w+)){1,}',  # 4 EL Something
    r'(\d+\s\w+).{2}(\(?\w+\)?)',  # 4 EL something, (something) Klammern optional
    r'^\w+$'  # Something
]


def parse_ingredients_regex(ingredients, rule_list, rule_lines):
    for ingredient in ingredients:
        regex_found = False

        for regex in regex_rules:
            match_object = re.match(regex, ingredient)

            if match_object is None:
                continue

            if max(match_object.regs, key=itemgetter(1))[-1] == len(ingredient):
                regex_found = True
                break
        if not regex_found:
            print(ingredient)
