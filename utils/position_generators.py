import math
import random

from utils import image_lib
from model import Ingredient, Pizza
import const


class PositionGenerator:
    def __init__(self):
        self.params = {}

    def generate_positions(self, pizza: Pizza, ingredient: Ingredient, ing_count: int) -> list[list[int]]:
        # method = getattr(self, ingredient.auto_place_method)
        method = self.random
        return method(pizza, ingredient, ing_count)

    def random(self, pizza: Pizza, ingredient: Ingredient, ing_count: int) -> list[list[int]]:
        image = image_lib.get_pixmap(ingredient.get_image_filename())
        item_radius = math.hypot(image.width() / 2, image.height() / 2) / const.PIZZA_MAX_DIAM_PIX * 40
        max_r = math.ceil(pizza.size / 2 - 1 - item_radius)
        results = []
        item_radius /= 2
        while ing_count:
            for _ in range(10):
                radius = random.randint(0, max_r * 10) / 10
                angle = math.radians(random.randint(0, 360))
                x = radius * math.cos(angle)
                y = radius * math.sin(angle)
                rotate_item = random.randint(0, 360)
                for ox, oy, _ in results:
                    if math.hypot(x - ox, y - oy) < item_radius:
                        break
                else:
                    break
            results.append([x, y, rotate_item])
            ing_count -= 1

        return results

    def circle(self, pizza: Pizza, ingredient: Ingredient, ing_count: int) -> list[list[int]]:
        return []

    def mosaic(self, pizza: Pizza, ingredient: Ingredient, ing_count: int) -> list[list[int]]:
        return []


pos_gen = PositionGenerator()
