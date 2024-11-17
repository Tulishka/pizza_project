from datetime import datetime

from const import MeasureUnit


class Model:
    table_name = ""

    def __init__(self, id):
        self.id = id

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

    def __init__(self, id: int, name: str, title: str, serving_size: int, measure_unit: MeasureUnit | str,
                 price: int, category_id: int, weight: int, count: int):
        super().__init__(id)
        self.name = name
        self.count = count
        self.serving_size = serving_size
        self.title = title
        self.measure_unit = measure_unit if isinstance(measure_unit, MeasureUnit) else MeasureUnit(measure_unit)

        self.price = price
        self.category_id = category_id
        self.weight = weight


class AddedIngredient(Model):
    table_name = "pizzas_ingredients"

    def __init__(self, id: int, pizza_id: int, ingredient_id: int, addition_order: int, count: int,
                 placement_method: str, rotation_angle: int, coord: tuple):
        super().__init__(id)
        self.ingredient_id = ingredient_id
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
