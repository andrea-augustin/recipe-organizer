import sqlite3


class sqlite_handler:
    def __init__(self, path):
        self.conn = sqlite3.connect(path)
        self.c = self.conn.cursor()

    def close_connection(self):
        self.conn.close()

    """
    SQLite get functions
    """

    def get_all_product_names_and_plural_forms_from_products_table(self):
        return self.c.execute("SELECT product_name, plural_form FROM products").fetchall()

    def get_entry_from_products_table_by_product_name(self, product_name):
        return self.c.execute("SELECT * FROM products WHERE product_name='" + product_name + "'").fetchone()

    def get_entry_from_products_table_by_plural_form(self, plural):
        return self.c.execute("SELECT * "
                              "FROM products "
                              "WHERE plural_form='" + plural + "'").fetchone()

    def get_entry_from_products_table_by_alt_spelling(self, spelling):
        return self.c.execute("SELECT products.id,products.product_name,products.plural_form "
                              "FROM products "
                              "INNER JOIN alternate_product_spelling ON products.id=alternate_product_spelling.products_id "
                              "WHERE alternate_product_spelling.product_spelling='" + spelling + "'").fetchone()

    def get_all_alternate_writings_from_alternate_product_spelling_table(self):
        return self.c.execute("SELECT products.product_name, alternate_product_spelling.product_spelling "
                              "FROM products "
                              "INNER JOIN alternate_product_spelling ON alternate_product_spelling.id=products.id").fetchall()

    def get_entry_from_alternate_product_spelling_table_by_product_spelling(self, spelling):
        return self.c.execute("SELECT id, products_id, product_spelling "
                              "FROM alternate_product_spelling "
                              "WHERE product_spelling='" + spelling + "'").fetchone()

    def get_all_products_and_their_writing_as_list_from_database(self):
        out = list()

        all_products = self.get_all_product_names_and_plural_forms_from_products_table()
        all_writings = self.get_all_alternate_writings_from_alternate_product_spelling_table()

        for product in all_products:
            out.append(product[0])

            if product[1] is None:
                continue

            out.append(product[1])

        for writing in all_writings:
            out.append(writing[1])

        return out

    def get_all_recipe_categories_from_recipe_categories_table(self):
        # TODO implement when the categories table has content
        pass

    """
    SQLite insert functions
    """

    def insert_product_into_product_table(self, product_name, plural):
        self.c.execute("INSERT INTO products (product_name, plural_form) VALUES(?,?)", (product_name, plural))
        self.conn.commit()

    def insert_alternate_writing_into_alternate_product_spelling_table(self, product_id, alternate_writing):
        self.c.execute("INSERT INTO alternate_product_spelling (products_id, product_spelling) VALUES (?,?)",
                       (product_id, alternate_writing))
        self.conn.commit()
