def get_alternate_spelling_name():
    return input("Schreibweise eingeben:\n")


def ask_for_product_name(prod_from_db):
    product_name = input("Namen des vorhandenen Produkts eingeben" + '\n')
    while product_name not in prod_from_db or product_name == "exit":
        product_name = input(
            "Der Name '" + product_name + "' konnte nicht gefunden werden. Anderer Name oder aufhören >>exit<<?" + "\n")

    return product_name


def ask_for_singular_and_plural_names(ingr_name):
    return tuple(input("Singular und Plural von: " + ingr_name + '\n').split(','))


def check_if_ingredient_is_in_db(sqlite_handler):
    ingredient_to_check = input("Name der Zutat zum Nachschlagen:\n")
    prod_id = sqlite_handler.get_entry_from_products_table_by_product_name(ingredient_to_check)

    if prod_id is None:
        return 0
    else:
        return prod_id


def handle_alternate_spelling_name(product_name, prod_from_db, sqlite_handler):
    alternate_spelling = get_alternate_spelling_name()
    product_id = sqlite_handler.get_entry_from_products_table_by_product_name(product_name)[0]
    sqlite_handler.insert_alternate_writing_into_alternate_product_spelling_table(product_id, alternate_spelling)
    prod_from_db.append(alternate_spelling)


def handle_new_product_name(new_product, prod_from_db, sqlite_handler):
    if new_product[1] == '':
        new_product = (new_product[0], None)

    sqlite_handler.insert_product_into_product_table(new_product)

    prod_from_db.append(new_product[0])

    if new_product[1] is not None:
        prod_from_db.append(new_product[1])


def handle_product_abfrage(ingr, prods_from_db, sqlite_handler):
    user_input_new_product_or_alt_writing = input(
        "Produkt ist >>neu<<, >>andere<< Schreibweise, Zutat >>suchen<<, oder >>skip<<? " + ingr + '\n')

    if user_input_new_product_or_alt_writing == "neu":

        new_product = ask_for_singular_and_plural_names(ingr)
        handle_new_product_name(new_product, prods_from_db, sqlite_handler)

        ask_alt_name = input("Andere Schreibweise hinzufügen? y/n \n")

        if ask_alt_name == 'n':
            return

        handle_alternate_spelling_name(new_product[0], prods_from_db, sqlite_handler)

    elif user_input_new_product_or_alt_writing == "andere":

        product_name = ask_for_product_name(prods_from_db)

        if product_name == "exit":
            return

        handle_alternate_spelling_name(product_name, prods_from_db, sqlite_handler)

    elif user_input_new_product_or_alt_writing == "suchen":
        id_of_product = check_if_ingredient_is_in_db(sqlite_handler)

        if id_of_product == 0:
            user_input_new_product_or_alt_writing = input(
                "Die eingegebene Zutat gibt's nicht. Nochmal >>suchen<< oder Suche abbrechen >>cancel<<?\n")

            while user_input_new_product_or_alt_writing == "suchen":
                id_of_product = check_if_ingredient_is_in_db(sqlite_handler)

                if id_of_product == 0:
                    user_input_new_product_or_alt_writing = input(
                        "Die eingegebene Zutat gibt's nicht. Nochmal >>suchen<< oder Suche abbrechen >>cancel<<?\n")

            if user_input_new_product_or_alt_writing == "cancel":
                handle_product_abfrage(ingr, prods_from_db, sqlite_handler)

        else:
            print("Die Zutat gibt's!")
            handle_product_abfrage(ingr, prods_from_db, sqlite_handler)
    else:
        return
