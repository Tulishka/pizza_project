from functools import cache

from db_init.create_db import get_db
from model import Model, Pizza


def get_model(model_class: type(Model)) -> dict[int, Model]:
    with get_db() as con:
        cur = con.cursor()

        res = cur.execute(f"SELECT * FROM {model_class.table_name}").fetchall()

        column_names = [description[0] for description in cur.description]
        id_column = column_names.index("id")

        return {
            values[id_column]: model_class(**dict(zip(column_names, values)))
            for values in res
        }


@cache
def get_model_cached(model_class: type(Model)) -> dict[int, Model]:
    return get_model(model_class)


@cache
def get_base_price(pizza: Pizza):
    with get_db() as con:
        cur = con.cursor()

        res = cur.execute(f""" 
            SELECT price 
            FROM base_prices
            WHERE 
                dought_tipe_id=? AND souse_id=? AND size=?
        """, (pizza.dough_type_id, pizza.souse_id, pizza.size)).fetchall()

    return res[0][0] if res else 0
