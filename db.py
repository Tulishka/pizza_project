import json
from functools import cache

from utils.create_db import get_db
from model import Model, Pizza
from utils.enums import OrderStatus


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


def insert_model(model: Model):
    with get_db() as con:
        cur = con.cursor()
        model_class = type(model)
        ins_keys = model.get_insert_fields()
        fields = ",".join(ins_keys)
        values = ",".join(repr(getattr(model, key)) for key in ins_keys)
        cur.execute(f"INSERT INTO {model_class.table_name} ({fields}) VALUES ({values})")
        res = cur.execute(f"SELECT last_insert_rowid()").fetchone()
        model.id = res[0]


def update_model(model: Model):
    with get_db() as con:
        cur = con.cursor()
        model_class = type(model)
        key_val = [(key, repr(getattr(model, key))) for key in model.get_insert_fields()]
        fields_values = ",".join(f"{key}={val}" for key, val in key_val)
        cur.execute(
            f"UPDATE {model_class.table_name} SET {fields_values} WHERE id=?", [model.id]
        )


@cache
def get_base_price(pizza: Pizza):
    with get_db() as con:
        cur = con.cursor()

        res = cur.execute(f""" 
            SELECT price FROM base_prices
            WHERE dought_tipe_id=? AND souse_id=? AND size=?
        """, (pizza.dough_type_id, pizza.souse_id, pizza.size)).fetchall()

    return res[0][0] if res else 0


def cancel_uncompleted_orders():
    with get_db() as con:
        cur = con.cursor()
        cur.execute(f""" 
            UPDATE orders SET status='{OrderStatus.CANCELED}' 
            WHERE status='{OrderStatus.NEW}'
        """)


def save_pizza(pizza: Pizza):
    insert_model(pizza)

    values = ",".join(
        f"({pizza.id},{ing.ingredient_id},{ing.addition_order},{ing.count},{ing.portion_size},'{json.dumps(ing.position)}')"
        for ing in pizza.added_ingredients
    )
    if pizza.added_ingredients:
        with get_db() as con:
            cur = con.cursor()
            cur.execute(f"""
            INSERT INTO pizzas_ingredients (pizza_id, ingredient_id, addition_order, count, portion_size, position)
            VALUES {values}
            """)
