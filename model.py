from datetime import datetime
from enum import Enum


class MeasureUnit(str, Enum):
    PIECES = "шт."
    GRAM = "гр."


class Model:
    def __init__(self, id):
        self.id = id


class IngredientCategory(Model):
    def __init__(self, id, title):
        super().__init__(id)
        self.title = title


class Ingredient(Model):
    def __init__(self, id: int, icon: str, img: str, count: int, serving_size: int, title: str,
                 measure_unit: MeasureUnit, price: int, category: IngredientCategory, weight: int):
        super().__init__(id)
        self.icon = icon
        self.img = img
        self.count = count
        self.serving_size = serving_size
        self.title = title
        self.measure_unit = measure_unit

        self.price = price
        self.category = category
        self.weight = weight


class AddedIngredient(Model):
    def __init__(self, id: int, ingredient: Ingredient, addition_order: int, count: int, placement_method: str, rotation_angle: int, coord: tuple):
        super().__init__(id)
        self.ingredient = ingredient
        self.addition_order = addition_order
        self.count = count
        self.placement_method = placement_method
        self.rotation_angle = rotation_angle
        self.coord = coord


class BaseIngredient(Model):
    def __init__(self, id: int, unit_weight: int, title: str, img: str):
        super().__init__(id)
        self.unit_weight = unit_weight
        self.title = title
        self.img = img


class DoughType(BaseIngredient):
    pass


class Sauce(BaseIngredient):
    pass


class Pizza(Model):
    def __init__(self, id: int, dough_type: DoughType, size: int, sauce: Sauce):
        super().__init__(id)
        self.dough_type = dough_type
        self.size = size
        self.souse = sauce
        self.added_ingredients = []


class Order(Model):
    def __init__(self, id: int, date: datetime, pizza: Pizza, status: str):
        super().__init__(id)
        self.date = date
        self.pizza = pizza
        self.status = status
