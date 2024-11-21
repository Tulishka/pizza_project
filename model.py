import json
import math
from datetime import datetime

from utils.enums import MeasureUnit


class Model:
    table_name = ""
    primary_key = "id"
    read_only_keys = []

    def __init__(self, id):
        self.id = id

    def get_insert_fields(self) -> list[str]:
        return [
            key
            for key in self.__dict__.keys()
            if key != self.primary_key and key[0] != '_' and key not in self.read_only_keys
        ]

    def __repr__(self):
        values = ",".join(f"{key}={repr(value)}" for key, value in self.__dict__.items())
        return f"{self.__class__.__name__}({values})"


class IngredientCategory(Model):
    table_name = "categories"

    def __init__(self, id, title):
        super().__init__(id)
        self.title = title


class Ingredient(Model):
    table_name = "ingredients"
    BIG_PORTION_MULTIPLIER = 1.5

    def __init__(self, id: int, name: str, title: str, serving_size: int, measure_unit: MeasureUnit | str,
                 price: int, category_id: int, weight: int, count: int, auto_place_method: str):
        super().__init__(id)
        self.name = name
        self.count = count
        self.serving_size = serving_size
        self.title = title
        self.measure_unit = measure_unit if isinstance(measure_unit, MeasureUnit) else MeasureUnit(measure_unit)
        self.auto_place_method = auto_place_method
        self.price = price
        self.category_id = category_id
        self.weight = weight

    def get_icon_filename(self):
        return f"ingredients/{self.name}_icon.png"

    def get_image_filename(self):
        return f"ingredients/{self.name}.png"

    def get_portion_size(self, portion_size):
        if not portion_size:
            return self.serving_size

        return math.ceil(self.serving_size * Ingredient.BIG_PORTION_MULTIPLIER)

    def get_portion_price(self, portion_size):
        if not portion_size:
            return self.price

        return math.ceil(self.price * Ingredient.BIG_PORTION_MULTIPLIER)


class AddedIngredient(Model):
    table_name = "pizzas_ingredients"

    def __init__(self, id: int, pizza_id: int, ingredient_id: int, addition_order: int, count: int,
                 portion_size: int, position: str | list[list[int]]):
        super().__init__(id)
        self.ingredient_id = ingredient_id
        self.pizza_id = pizza_id
        self.addition_order = addition_order
        self.count = count
        self.portion_size = portion_size
        self.position = json.loads(position) if type(position) is str else position


class BaseIngredient(Model):
    def __init__(self, id: int, unit_weight: float, title: str, img: str):
        super().__init__(id)
        self.unit_weight = unit_weight
        self.title = title
        self.img = img


class DoughType(BaseIngredient):
    table_name = "dough_types"


class Souse(BaseIngredient):
    table_name = "souses"


class Pizza(Model):
    table_name = "pizzas"
    read_only_keys = "added_ingredients"

    def __init__(self, id: int, dough_type_id: int, size: int, souse_id: int):
        super().__init__(id)
        self.dough_type_id = dough_type_id
        self.size = size
        self.souse_id = souse_id
        self.added_ingredients: list[AddedIngredient] = []


class Order(Model):
    table_name = "orders"

    def __init__(self, id: int | None, date: str, pizza_id: int, total_sum: int, status: str):
        super().__init__(id)
        self.date = date
        self.pizza_id = pizza_id
        self.status = status
        self.total_sum = total_sum
