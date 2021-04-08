class ingredientElement:
    def __init__(self):
        self.amount = 0
        self.amount_type = ""
        self.ingredient_name = ""


class parserElement:
    def __init__(self, ingredient, current_pos, ingredient_element):
        self.ingredient = ingredient
        self.pos = current_pos
        self.ingredient_element = ingredient_element