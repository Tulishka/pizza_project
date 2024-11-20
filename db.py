from functools import cache

from create_db import get_db
from model import Model, Ingredient, IngredientCategory


def get_model(model_class: type(Model)) -> dict[int, Model]:
    with get_db() as con:
        cur = con.cursor()

        res = cur.execute(f""" 
            SELECT * 
            FROM {model_class.table_name}
        """).fetchall()

        column_names = [description[0] for description in cur.description]

        id_column = column_names.index("id")

        return {
            values[id_column]: model_class(**dict(zip(column_names, values)))
            for values in res
        }


@cache
def get_model_cached(model_class: type(Model)) -> dict[int, Model]:
    return get_model(model_class)
