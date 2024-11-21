from PyQt6.QtGui import QPixmap

import db
from model import Pizza, Ingredient, DoughType, Souse


class State:
    current_pizza: Pizza = Pizza(0, 1, 40, 1)
    pizza_image: QPixmap
    pizza_image_file: str


def current_pizza() -> Pizza:
    return State.current_pizza


def new_pizza(dough_type: int, size: int, souse: int):
    State.current_pizza = Pizza(0, dough_type, size, souse)


def current_pizza_total_cost() -> int:
    total_sum = db.get_base_price(current_pizza())
    for ingredient in current_pizza().added_ingredients:
        total_sum += all_ingredients_dict[ingredient.ingredient_id].get_portion_price(ingredient.portion_size)
    return total_sum


def current_pizza_ingredients_count() -> int:
    return len(current_pizza().added_ingredients)


all_ingredients_dict = db.get_model_cached(Ingredient)
all_dough_dict = db.get_model_cached(DoughType)
all_souses_dict = db.get_model_cached(Souse)


def set_pizza_picture(filename, capturedImage):
    State.pizza_image_file = filename
    State.pizza_image = capturedImage
