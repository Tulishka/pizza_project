from PyQt6.QtGui import QPainter, QImage
from PyQt6.QtWidgets import QWidget, QSizePolicy

import images_rep
from db import get_model_cached
from model import Ingredient, current_pizza, PIZZA_MAX_SIZE_PIX, PIZZA_SIZE_KOEF, PIZZA_MAX_DIAM_PIX


class PizzaWidget(QWidget):

    def __init__(self, parent):
        super().__init__(parent)
        self.setObjectName("pizzaWidget")
        # self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.setMinimumSize(PIZZA_MAX_SIZE_PIX, PIZZA_MAX_SIZE_PIX)

        w = int(PIZZA_MAX_SIZE_PIX * PIZZA_SIZE_KOEF[current_pizza.size])
        h = int(PIZZA_MAX_SIZE_PIX * PIZZA_SIZE_KOEF[current_pizza.size])

        self.pizza_base = QImage(f"images/ingredients/{'pizza_big_base'}.png")
        self.pizza_base = self.pizza_base.scaled(w, h)

        self.souse_img = QImage(f"images/ingredients/{'tomato_souse'}.png")
        self.souse_img = self.souse_img.scaled(w, h)

        self.all_ingredients_dict = get_model_cached(Ingredient)

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        cx, cy = self.width() // 2, self.height() // 2
        qp.drawImage(cx - self.pizza_base.width() // 2, cy - self.pizza_base.height() // 2, self.pizza_base)
        qp.drawImage(cx - self.pizza_base.width() // 2, cy - self.pizza_base.height() // 2, self.souse_img)

        for ad_ing in current_pizza.added_ingredients:
            ing = self.all_ingredients_dict[ad_ing.ingredient_id]
            img = images_rep.get_image(ing.get_image_filename())
            w, h = img.width() / 2, img.height() / 2
            for x, y, angle in ad_ing.position:
                x = x * PIZZA_MAX_DIAM_PIX / 40
                y = y * PIZZA_MAX_DIAM_PIX / 40
                qp.drawImage(int(cx + x - w), int(cy + y - h), img)

        qp.end()
        super().paintEvent(event)
