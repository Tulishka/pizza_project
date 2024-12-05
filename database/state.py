"""Файл содержит функции для работы с текущим состоянием (текущая пицца, текущий заказ)"""

from PyQt6.QtGui import QPixmap
from datetime import datetime

from database import db
from database.db import update_model
from database.model import Pizza, Ingredient, DoughType, Souse, Order
from utils.enums import OrderStatus


class State:
    """Класс для хранения экземпляра пиццы и заказа, используется в качестве синглтона"""

    current_pizza: Pizza = Pizza(0, 1, 40, 1)
    order: Order = None
    pizza_image: QPixmap = None
    pizza_image_file: str


def current_pizza() -> Pizza:
    return State.current_pizza


def new_order():
    """Обработчик создания нового заказа
    :return None:
    """
    # Отмена незавершённых заказов
    db.cancel_uncompleted_orders()

    # Создание и запись нового заказа
    State.order = Order(0, datetime.now().isoformat(), 0, 0, OrderStatus.NEW)
    db.insert_model(State.order)


def new_pizza(dough_type_id: int, size_cm: int, souse_id: int):
    State.current_pizza = Pizza(0, dough_type_id, size_cm, souse_id)


def current_pizza_total_cost() -> int:
    """Функция расчёта итоговой стоимости пиццы
    :return int:
    """
    total_sum = db.get_base_price(current_pizza())
    for ingredient in current_pizza().added_ingredients:
        total_sum += all_ingredients_dict[ingredient.ingredient_id].get_portion_price(ingredient.portion_size)
    return total_sum


def current_pizza_ingredients_count() -> int:
    """Функция считает текущее количество ингредиентов в текущей пицце
    :return int:
    """
    return len(current_pizza().added_ingredients)


def set_pizza_picture(filename, captured_image):
    """Функция сохраняет в state изображение пиццы
    :param filename:
    :param captured_image:
    :return None:
    """
    State.pizza_image_file = filename
    State.pizza_image = captured_image


def save_order(pizza: Pizza, total_sum: int):
    """Функция сохраняет пиццу в БД, обновляет и сохраняет заказ
    :param pizza:
    :param total_sum:
    :return None:
    """
    db.save_pizza(pizza)
    State.order.pizza_id = pizza.id
    State.order.total_sum = total_sum
    update_model(State.order)


def order_complete():
    """Функция завершает заказ: устанавливает ему статус оплачен
    :return None:
    """
    State.order.status = OrderStatus.PAYED
    update_model(State.order)

# чтение ингредиентов из БД
all_ingredients_dict = db.get_model_cached(Ingredient)
all_dough_dict = db.get_model_cached(DoughType)
all_souses_dict = db.get_model_cached(Souse)
