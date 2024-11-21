from enum import Enum


class MeasureUnit(str, Enum):
    PIECES = "шт."
    GRAM = "гр."

    def __str__(self):
        return self.value

    def __repr__(self):
        return f"'{self.value}'"


class OrderStatus(str, Enum):
    NEW = "НОВЫЙ"
    PAYED = "ОПЛАЧЕН"
    CANCELED = "ОТМЕНЕН"

    def __str__(self):
        return self.value

    def __repr__(self):
        return f"'{self.value}'"
