"""
В этом файле находятся классы моделей, которые представляют собой таблицы в БД
"""

import json
import math
from datetime import datetime

from utils.enums import MeasureUnit


class Model:
    """Базовый класс, от него наследуются другие классы моделей"""

    table_name = ""
    primary_key = "id"
    read_only_keys = []

    def __init__(self, id):
        self.id = id

    def get_insert_fields(self) -> list[str]:
        """Функция возвращает список полей для вставки/записи
        :return list[str]:
        """
        return [
            key
            for key in self.__dict__.keys()
            if key != self.primary_key and key[0] != '_' and key not in self.read_only_keys
        ]

    def __repr__(self):
        values = ",".join(f"{key}={repr(value)}" for key, value in self.__dict__.items())
        return f"{self.__class__.__name__}({values})"


class IngredientCategory(Model):
    """Модель категории ингредиентов"""

    table_name = "categories"

    def __init__(self, id, title):
        super().__init__(id)
        self.title = title


class Ingredient(Model):
    """Модель ингредиента"""

    table_name = "ingredients"
    BIG_PORTION_MULTIPLIER = 1.5

    def __init__(self, id: int, name: str, title: str, serving_size: int, measure_unit: MeasureUnit | str,
                 price: int, category_id: int, weight: int, count: int, auto_place_method: str):
        """
        :param id:
        :param name: уникальное английское имя ингредиента (используется в имени файла картинки)
        :param title: отображаемое название ингредиента
        :param serving_size: количество кусочков в стандартной порции
        :param measure_unit: единица измерения
        :param price: цена за порцию
        :param category_id: id категории
        :param weight: вес порции в граммах
        :param count: количество на складе
        :param auto_place_method: способ начального размещения кусочков на пицце
        """
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

    def get_portion_size(self, portion_size) -> int:

        if not portion_size:
            return self.serving_size

        return math.ceil(self.serving_size * Ingredient.BIG_PORTION_MULTIPLIER)

    def get_portion_price(self, portion_size):
        """Функция считает и возвращает цену за порцию
        :param portion_size:
        :return:
        """
        if not portion_size:
            return self.price

        return math.ceil(self.price * Ingredient.BIG_PORTION_MULTIPLIER)


class AddedIngredient(Model):
    """Модель добавленных на пиццу ингредиентов"""

    table_name = "pizzas_ingredients"

    def __init__(self, id: int, pizza_id: int, ingredient_id: int, addition_order: int, count: int,
                 portion_size: int, position: str | list[list[int]]):
        """
        :param id:
        :param pizza_id: id пиццы
        :param ingredient_id: id ингредиента
        :param addition_order: порядок добавления ингредиента
        :param count: количество добавленных кусочков
        :param portion_size: размер порции (0 - стандартная, 1 - большая)
        :param position: позиции кусочков в виде списка, где каждый кусочек представлен в виде [x, y, угол-поворота]
                         например для 3 кусочков: [[1,1,90], [0,1,0], [0,0,180]] - коорд. в см. угол  - в градусах.
        """
        super().__init__(id)
        self.ingredient_id = ingredient_id
        self.pizza_id = pizza_id
        self.addition_order = addition_order
        self.count = count
        self.portion_size = portion_size
        self.position = json.loads(position) if type(position) is str else position


class BaseIngredient(Model):
    """Базовый класс основного ингредиента пиццы (тесто, соус) """

    def __init__(self, id: int, unit_weight: float, title: str, img: str):
        """
        :param id:
        :param unit_weight: вес на единицу площади
        :param title: название
        :param img:
        """
        super().__init__(id)
        self.unit_weight = unit_weight
        self.title = title
        self.img = img


class DoughType(BaseIngredient):
    """Модель Тип теста"""
    table_name = "dough_types"


class Souse(BaseIngredient):
    """Модель вид соуса"""
    table_name = "souses"


class Pizza(Model):
    """Класс модели пиццы"""

    table_name = "pizzas"
    read_only_keys = ["added_ingredients"]

    def __init__(self, id: int, dough_type_id: int, size: int, souse_id: int):
        """
        :param id:
        :param dough_type_id: id типа теста
        :param size: размер в см
        :param souse_id: id соуса
        """
        super().__init__(id)
        self.dough_type_id = dough_type_id
        self.size = size
        self.souse_id = souse_id
        self.added_ingredients: list[AddedIngredient] = []


class Order(Model):
    """Класс модели заказа"""
    table_name = "orders"

    def __init__(self, id: int | None, date: str, pizza_id: int, total_sum: int, status: str):
        """
        :param id:
        :param date: дата создания заказа
        :param pizza_id: id пиццы
        :param total_sum: итоговая сумма
        :param status: статус заказа
        """
        super().__init__(id)
        self.date = date
        self.pizza_id = pizza_id
        self.status = status
        self.total_sum = total_sum
