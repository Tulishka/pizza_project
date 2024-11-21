from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QImage
from PyQt6.QtWidgets import QWidget, QSizePolicy

import images_rep
from db import get_model_cached
from model import Ingredient, current_pizza, PIZZA_MAX_SIZE_PIX, PIZZA_SIZE_KOEF, PIZZA_MAX_DIAM_PIX


class PizzaComponent:
    def __init__(self, image: QImage, ingredient_index: int, item_index: int):
        self.image = image
        self.ingredient_index = ingredient_index
        self.item_index = item_index


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

        self.dragging = None

        self.setUpdatesEnabled(True)

        self.components = []

    def setup_components(self):
        self.components = []
        for ing_ind, ad_ing in enumerate(current_pizza.added_ingredients):
            ing = self.all_ingredients_dict[ad_ing.ingredient_id]
            img = images_rep.get_image(ing.get_image_filename())

            for i in range(ad_ing.count):
                self.components.append(PizzaComponent(img, ing_ind, i))

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

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            cx, cy = self.width() // 2, self.height() // 2
            pos = event.position()
            print(pos)
            for comp in self.components:
                ad_ing = current_pizza.added_ingredients[comp.ingredient_index]

                x = ad_ing.position[comp.item_index][0]
                y = ad_ing.position[comp.item_index][1]
                angle = ad_ing.position[comp.item_index][2]

                x = x * PIZZA_MAX_DIAM_PIX / 40 - comp.image.width() / 2
                y = y * PIZZA_MAX_DIAM_PIX / 40 - comp.image.height() / 2

                ix, iy = int(pos.x() - x - cx), int(pos.y() - y - cy)
                # print(comp.image.pixelColor(ix, iy).alpha())

                if (x + cx <= pos.x() <= x + cx + comp.image.width() and
                        y + cy <= pos.y() <= y + cy + comp.image.height() and
                        comp.image.pixelColor(ix, iy).alpha() > 0):
                    self.dragging = comp
                    self.offset_x = pos.x() - x
                    self.offset_y = pos.y() - y

    def mouseMoveEvent(self, event):
        if self.dragging:
            pos = event.position()

            x = int(pos.x() - self.offset_x)
            y = int(pos.y() - self.offset_y)

            x = x + self.dragging.image.width() / 2
            y = y + self.dragging.image.height() / 2
            x = x / PIZZA_MAX_DIAM_PIX * 40
            y = y / PIZZA_MAX_DIAM_PIX * 40

            ad_ing = current_pizza.added_ingredients[self.dragging.ingredient_index]

            ad_ing.position[self.dragging.item_index][0] = x
            ad_ing.position[self.dragging.item_index][1] = y

            self.update()  # Обновляем виджет для перерисовки

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = None
