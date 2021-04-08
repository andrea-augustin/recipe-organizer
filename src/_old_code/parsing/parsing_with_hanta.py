from HanTa.HanoverTagger import HanoverTagger
from nltk import word_tokenize

from src._old_code.parsing import parser_grammar, parsing_elements

tagger = HanoverTagger('../../data/resources/morphmodel_ger.pgz')

hanta_ingredients_list = []


def hanta_parse_terminals(parser_element, rule_left_side):
    if parser_element.ingredient[parser_element.pos][-1] == 'CARD' and rule_left_side == parser_grammar.grammar_number:
        if parser_element.ingredient_element.amount == 0:
            parser_element.ingredient_element.amount = int(parser_element.ingredient[parser_element.pos][0])
            parser_element.pos += 1
            return True
        else:
            # spezifizierer für zutat (à ....)
            print("what to do...")
    # ZUTAT
    elif parser_element.ingredient[parser_element.pos][
        -1] == 'NN' and rule_left_side == parser_grammar.grammar_ingredient_name:
        print("what to do...")
    # MENGENART
    elif parser_element.ingredient[parser_element.pos][
        -1] == 'NE' and rule_left_side == parser_grammar.grammar_amount_type:
        print("what to do...")
    elif parser_element.ingredient[parser_element.pos][-1] in ['ADJA', 'ADJD']:
        print("what to do...")
    else:
        return False


def hanta_parse_rule(parser_element, rule_right_side, parsing_path):
    if len(rule_right_side) == 0:
        return False

    for outside_cnt, rule in enumerate(rule_right_side):
        rule_parsed = False
        parsing_path.append(rule)
        rule_pos = 0
        for cnt, rule_rule in enumerate(rule):
            if rule_rule not in parser_grammar.non_terminals:
                rule_parsed = hanta_parse_terminals(parser_element, rule_rule)
            else:
                rule_parsed = hanta_parse_rule(parser_element, parser_grammar.grammar[rule_rule], parsing_path)

            rule_pos += 1

            if rule_parsed and rule_pos == len(rule):
                return True
            else:
                if cnt + 1 == len(rule):
                    parsing_path = parsing_path[:-1]

                continue
        if (rule_parsed is False or rule_parsed is None) and rule == parsing_path[-1]:
            parsing_path = parsing_path[:-1]


def hanta_parse_ingredients_main(ingredient):
    current_pos = 0
    parser_element = parsing_elements.parserElement(ingredient, current_pos, parsing_elements.ingredientElement())

    # parse_rule(parser_element, grammar[grammar_s], [['S']])


def parse_ingredients_hanta(ingredients):
    for ingredient in ingredients:
        out = []
        tokenized_ingredient = word_tokenize(ingredient)
        tagged_ingredient = tagger.tag_sent(tokenized_ingredient)

        for tagged in tagged_ingredient:
            if tagged[0].isnumeric():
                continue

            if tagged[0].lower() in parser_grammar.grammar[parser_grammar.grammar_amount_type]:
                continue

            if '$' in tagged[-1]:
                continue

            if 'à' in tagged[0]:
                continue

            out.append(tagged[1])

        if out not in hanta_ingredients_list:
            hanta_ingredients_list.append(out)
        # print(tagged_ingredient)
        # parse_ingredients_main(tagged_ingredient)
