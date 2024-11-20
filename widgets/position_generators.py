import math

import images_rep
from model import Ingredient, Pizza


class PositionGenerator:
    def __init__(self):
        self.params = {}

    def gen_ingredient_positions(self, pizza: Pizza, ingredient: Ingredient, ing_count: int) -> list[list[int]]:
        method = getattr(self, ingredient.auto_place_method)
        return method(pizza, ingredient, ing_count)

    def random(self, pizza: Pizza, ingredient: Ingredient, ing_count: int) -> list[list[int]]:
        image = images_rep.get_pixmap(ingredient.get_image_filename())
        max_r = pizza.size / 2 - 1 - math.hypot(image.width() / 2, image.height() / 2)

        while ing_count:
            ing_count -= 1

        return []

    def circle(self, pizza: Pizza, ingredient: Ingredient, ing_count: int) -> list[list[int]]:
        return []

    def mosaic(self, pizza: Pizza, ingredient: Ingredient, ing_count: int) -> list[list[int]]:
        return []
