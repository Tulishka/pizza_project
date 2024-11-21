from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QImage, QTransform
from PyQt6.QtWidgets import QWidget, QSizePolicy, QSlider

import images_rep
from db import get_model_cached
from model import Ingredient, current_pizza, PIZZA_MAX_SIZE_PIX, PIZZA_SIZE_KOEF, PIZZA_MAX_DIAM_PIX


class PizzaComponent:
    def __init__(self, image: QImage, ingredient_index: int, item_index: int):
        self.src_image = image
        self.image = image
        self.ingredient_index = ingredient_index
        self.item_index = item_index

        self.applied_angle = 0

    def get_image(self, angle):
        if self.applied_angle != angle:
            self.applied_angle = angle
            self.image = self.src_image.transformed(QTransform().rotate(angle))

        return self.image


class PizzaWidget(QWidget):

    def __init__(self, parent):
        super().__init__(parent)
        self.setObjectName("pizzaWidget")
        self.setMinimumSize(PIZZA_MAX_SIZE_PIX, PIZZA_MAX_SIZE_PIX)



        self.all_ingredients_dict = get_model_cached(Ingredient)

        self.dragging = None
        self.last_item = None

        self.setUpdatesEnabled(True)

        self.angleSlider = QSlider(Qt.Orientation.Horizontal, self)
        self.angleSlider.setMinimum(-180)
        self.angleSlider.setMaximum(180)
        self.angleSlider.hide()
        sw = 100
        sh = 30
        self.angleSlider.setGeometry(
            parent.width() // 2 - sw // 2,
            parent.height() - 120,
            sw, sh)
        self.angleSlider.valueChanged.connect(self.slider_changed)

        self.components = []


    def setup_pizza_base(self):
        w = int(PIZZA_MAX_SIZE_PIX * PIZZA_SIZE_KOEF[current_pizza().size])
        h = int(PIZZA_MAX_SIZE_PIX * PIZZA_SIZE_KOEF[current_pizza().size])

        self.pizza_base = QImage(f"images/ingredients/{'pizza_big_base'}.png")
        self.pizza_base = self.pizza_base.scaled(w, h)

        self.souse_img = QImage(f"images/ingredients/{'tomato_souse'}.png")
        self.souse_img = self.souse_img.scaled(w, h)

    def setup_components(self):
        self.components = []
        for ing_ind, ad_ing in enumerate(current_pizza().added_ingredients):
            ing = self.all_ingredients_dict[ad_ing.ingredient_id]
            img = images_rep.get_image(ing.get_image_filename())

            for i in range(ad_ing.count):
                self.components.append(PizzaComponent(img, ing_ind, i))
        self.last_item = None
        self.angleSlider.hide()

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        cx, cy = self.width() // 2, self.height() // 2
        qp.drawImage(cx - self.pizza_base.width() // 2, cy - self.pizza_base.height() // 2, self.pizza_base)
        qp.drawImage(cx - self.pizza_base.width() // 2, cy - self.pizza_base.height() // 2, self.souse_img)

        for comp in self.components:
            ad_ing = current_pizza().added_ingredients[comp.ingredient_index]
            x, y, angle = ad_ing.position[comp.item_index]
            img = comp.get_image(angle)
            w, h = img.width() / 2, img.height() / 2
            x = x * PIZZA_MAX_DIAM_PIX / 40
            y = y * PIZZA_MAX_DIAM_PIX / 40
            qp.drawImage(int(cx + x - w), int(cy + y - h), img)

        qp.end()
        super().paintEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            cx, cy = self.width() // 2, self.height() // 2
            pos = event.position()
            for comp in reversed(self.components):
                ad_ing = current_pizza().added_ingredients[comp.ingredient_index]
                x, y, angle = ad_ing.position[comp.item_index]
                img = comp.get_image(angle)

                x = x * PIZZA_MAX_DIAM_PIX / 40 - comp.image.width() / 2
                y = y * PIZZA_MAX_DIAM_PIX / 40 - comp.image.height() / 2

                ix, iy = int(pos.x() - x - cx), int(pos.y() - y - cy)

                if (x + cx <= pos.x() <= x + cx + img.width() and
                        y + cy <= pos.y() <= y + cy + img.height() and
                        img.pixelColor(ix, iy).alpha() > 0):
                    self.dragging = comp
                    self.offset_x = pos.x() - x
                    self.offset_y = pos.y() - y
                    self.last_item = ad_ing, comp.item_index
                    self.angleSlider.setValue(angle - 360 if abs(angle) > 180 else angle)
                    self.angleSlider.show()
                    break

    def mouseMoveEvent(self, event):
        if self.dragging:
            pos = event.position()

            x = int(pos.x() - self.offset_x)
            y = int(pos.y() - self.offset_y)

            x = x + self.dragging.image.width() / 2
            y = y + self.dragging.image.height() / 2
            x = x / PIZZA_MAX_DIAM_PIX * 40
            y = y / PIZZA_MAX_DIAM_PIX * 40

            ad_ing = current_pizza().added_ingredients[self.dragging.ingredient_index]

            ad_ing.position[self.dragging.item_index][0] = x
            ad_ing.position[self.dragging.item_index][1] = y

            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = None


    def slider_changed(self):
        slider = self.sender()
        if self.last_item is not None:
            self.last_item[0].position[self.last_item[1]][2] = slider.value()
            self.update()
