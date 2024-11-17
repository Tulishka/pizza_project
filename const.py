from enum import Enum


class MeasureUnit(str, Enum):
    PIECES = "шт."
    GRAM = "гр."

    def __str__(self):
        return self.value