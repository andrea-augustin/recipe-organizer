def parse_ingredients_spacy(ingredients, nlp, rule_list, rule_lines):
    for ingredient in ingredients:
        doc = nlp(ingredient)
        # print(' '.join('{word}/{tag}'.format(word=t.orth_, tag=t.pos_) for t in doc))
        rule = [t.pos_ for t in doc]
        words = [t.orth_ for t in doc]

        if rule not in rule_list:
            rule_list.append(rule)
            rule_lines[tuple(rule)] = [words]
        else:
            if words not in rule_lines[tuple(rule)]:
                rule_lines[tuple(rule)].append(words)