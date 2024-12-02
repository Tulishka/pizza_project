"""Файл содержит классы-перечисления"""

from enum import Enum


class MeasureUnit(str, Enum):
    """Единицы измерения"""

    PIECES = "шт."
    GRAM = "гр."

    def __str__(self):
        return self.value

    def __repr__(self):
        return f"'{self.value}'"


class OrderStatus(str, Enum):
    """Статусы заказа"""

    NEW = "НОВЫЙ"
    PAYED = "ОПЛАЧЕН"
    CANCELED = "ОТМЕНЕН"

    def __str__(self):
        return self.value

    def __repr__(self):
        return f"'{self.value}'"
