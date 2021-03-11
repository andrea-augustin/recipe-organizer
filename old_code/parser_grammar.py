grammar_s = "S"
grammar_ingredient_info = "ZUTATENANGABE"
grammar_amount_info = "MENGENANGABE"
grammar_ingredient_specifier = "ZUTATSPEZIFIZIERER"
grammar_ingredient_name = "ZUTAT"
grammar_amount_type = "MENGENART"
grammar_number = "ZAHLENART"

non_terminals = [
    grammar_s,
    grammar_ingredient_info,
    grammar_amount_info,
    grammar_ingredient_specifier
]

grammar = {
    grammar_s: [
        [grammar_ingredient_info],
        [grammar_amount_info, grammar_ingredient_info]
    ],

    grammar_ingredient_info: [
        [grammar_ingredient_name],
        [grammar_ingredient_specifier, grammar_ingredient_name]
    ],

    grammar_amount_info: [
        [grammar_number],
        [grammar_number, grammar_amount_type]
    ],

    # Tag: NE oder NN
    grammar_amount_type: [
        'g', 'kg', 'lb', 'ml', 'l', 'cups', 'cup', 'el', 'tl', 'ml', 'tbsp', 'tsp', 'stiele', 'stiel', 'zweige',
        'zweig', 'dosen', 'dose', 'blatt', 'blätter', 'bund', 'cl'
    ],

    grammar_ingredient_name: [

    ],

    grammar_ingredient_specifier: [

    ],

    grammar_number: [

    ]
}
