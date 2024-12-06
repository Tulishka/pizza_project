import math

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QImage, QTransform
from PyQt6.QtWidgets import QWidget, QSlider

from database import state
from database.state import current_pizza
from utils import image_lib, const
from utils.image_lib import get_image


class PizzaComponent:
    """Отображаемый кусочек ингредиента на пицце"""

    def __init__(self, image: QImage, ingredient_index: int, item_index: int):
        """
        :param image: изображение кусочка
        :param ingredient_index: индекс ингредиента в списке ингредиентов
        :param item_index: индекс кусочка (от 0 до количества в порции)
        """
        self.src_image = image
        self.image = image
        self.ingredient_index = ingredient_index
        self.item_index = item_index

        self.applied_angle = 0

    def get_image(self, angle: int) -> QImage:
        """Метод возвращает изображение кусочка, повёрнутое на заданный угол
        :param angle:
        :return QImage:
        """
        if self.applied_angle != angle:
            self.applied_angle = angle
            self.image = self.src_image.transformed(QTransform().rotate(angle))

        return self.image


class PizzaWidget(QWidget):
    """Виджет для отображения пиццы на экране редактора"""

    def __init__(self, parent):
        super().__init__(parent)
        self.setObjectName("pizzaWidget")
        self.setMinimumSize(const.PIZZA_MAX_SIZE_PIX, const.PIZZA_MAX_SIZE_PIX)

        self.dragging = None
        self.last_item = None

        self.setUpdatesEnabled(True)

        self.angleSlider = QSlider(Qt.Orientation.Horizontal, self)
        self.angleSlider.setMinimum(-180)
        self.angleSlider.setMaximum(180)
        self.angleSlider.hide()
        slider_width = 100
        slider_height = 30
        self.angleSlider.setGeometry(
            parent.width() // 2 - slider_width // 2,
            parent.height() - 120,
            slider_width, slider_height)
        self.angleSlider.valueChanged.connect(self.slider_changed)

        # Кусочки ингредиентов
        self.components = []

    def setup_pizza_base(self):
        """Метод настройки базы пиццы, загружает и масштабирует картинки основы и соуса
        :return None:
        """
        w = int(const.PIZZA_MAX_SIZE_PIX * const.PIZZA_SIZE_KOEF[current_pizza().size])
        h = int(const.PIZZA_MAX_SIZE_PIX * const.PIZZA_SIZE_KOEF[current_pizza().size])

        self.pizza_base = get_image(f"ingredients/{state.all_dough_dict[current_pizza().dough_type_id].img}")
        self.pizza_base = self.pizza_base.scaled(w, h)

        self.souse_img = get_image(f"ingredients/{state.all_souses_dict[current_pizza().souse_id].img}")
        self.souse_img = self.souse_img.scaled(w, h)

    def setup_components(self):
        """Наполняет список компонентов (кусочков) пиццы
        :return None:
        """
        self.components = []
        for ing_ind, ad_ing in enumerate(current_pizza().added_ingredients):
            ing = state.all_ingredients_dict[ad_ing.ingredient_id]
            img = image_lib.get_image(ing.get_image_filename())

            for i in range(ad_ing.count):
                self.components.append(PizzaComponent(img, ing_ind, i))
        self.last_item = None
        self.angleSlider.hide()

    def paintEvent(self, event):
        """Обработчик события отрисовки виджета, рисует пиццу
        :param event:
        :return None:
        """
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
            x = x * const.PIZZA_MAX_DIAM_PIX / const.PIZZA_MAX_SIZE_CM
            y = y * const.PIZZA_MAX_DIAM_PIX / const.PIZZA_MAX_SIZE_CM
            qp.drawImage(int(cx + x - w), int(cy + y - h), img)

        qp.end()
        super().paintEvent(event)

    def keyPressEvent(self, event):
        """Обработчик нажатия кнопок
        :param event:
        :return None:
        """
        if event.key() == Qt.Key.Key_Q:
            if self.last_item is not None:
                self.angleSlider.setValue(self.angleSlider.value() - 25)
                self.last_item_set_angle(self.angleSlider.value())
        elif event.key() == Qt.Key.Key_E:
            if self.last_item is not None:
                self.angleSlider.setValue(self.angleSlider.value() + 25)
                self.last_item_set_angle(self.angleSlider.value())
        else:
            super().keyPressEvent(event)

    def mousePressEvent(self, event):
        """Обработчик нажатия мыши на поле пиццы
        :param event:
        :return None:
        """
        if event.button() == Qt.MouseButton.LeftButton:
            cx, cy = self.width() // 2, self.height() // 2
            pos = event.position()

            # Ищем кусочек, который находится под указателем мыши
            for comp in reversed(self.components):
                ad_ing = current_pizza().added_ingredients[comp.ingredient_index]
                x, y, angle = ad_ing.position[comp.item_index]
                img = comp.get_image(angle)

                x = x * const.PIZZA_MAX_DIAM_PIX / const.PIZZA_MAX_SIZE_CM - comp.image.width() / 2
                y = y * const.PIZZA_MAX_DIAM_PIX / const.PIZZA_MAX_SIZE_CM - comp.image.height() / 2

                ix, iy = int(pos.x() - x - cx), int(pos.y() - y - cy)

                # проверяем, что координаты мыши указывают текущий кусочек
                if (x + cx <= pos.x() <= x + cx + img.width() and
                        y + cy <= pos.y() <= y + cy + img.height() and
                        img.pixelColor(ix, iy).alpha() > 0):
                    # захватываем подходящий кусочек для перемещения
                    self.dragging = comp
                    self.offset_x = pos.x() - x
                    self.offset_y = pos.y() - y
                    self.last_item = ad_ing, comp.item_index
                    self.angleSlider.setValue(angle - 360 if abs(angle) > 180 else angle)
                    self.angleSlider.show()
                    self.angleSlider.setFocus()
                    break

    def mouseMoveEvent(self, event):
        """Обработчик перемещения мыши по полю пиццы,
        если есть захваченный кусочек (self.dragging) то изменяем его координаты"""
        if self.dragging:
            pos = event.position()

            x = int(pos.x() - self.offset_x)
            y = int(pos.y() - self.offset_y)

            # Перевод координат в систему отсчета (0, 0) - центр пиццы
            x = x + self.dragging.image.width() / 2
            y = y + self.dragging.image.height() / 2

            # Перевод координат из пикселей в сантиметры
            x = x / const.PIZZA_MAX_DIAM_PIX * const.PIZZA_MAX_SIZE_CM
            y = y / const.PIZZA_MAX_DIAM_PIX * const.PIZZA_MAX_SIZE_CM

            # Проверка, что кусочек выходит за радиус пиццы
            item_radius = math.hypot(self.dragging.image.width() / 2, self.dragging.image.height() / 2)
            item_radius = item_radius / const.PIZZA_MAX_DIAM_PIX * const.PIZZA_MAX_SIZE_CM
            max_radius = current_pizza().size / 2 - item_radius / 2
            cur_radius = math.hypot(x, y)
            if cur_radius > max_radius:
                # Корректировка координат, если выходит за радиус
                x = x / cur_radius * max_radius
                y = y / cur_radius * max_radius

            ad_ing = current_pizza().added_ingredients[self.dragging.ingredient_index]

            # Сохранение новых координат кусочка в добавленном ингредиенте
            ad_ing.position[self.dragging.item_index][0] = x
            ad_ing.position[self.dragging.item_index][1] = y

            self.update()

    def mouseReleaseEvent(self, event):
        """Обработчик события, когда кнопка мыши отпущена,
        если был захвачен кусочек, отпускаем его
        :param event:
        :return None:
        """
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = None

    def slider_changed(self):
        """Обработчик изменения слайдера угла поворота.
        :return None:
        """
        slider = self.sender()
        self.last_item_set_angle(slider.value())


    def last_item_set_angle(self, angle):
        """Изменяем угол поворота для последнего захваченного кусочка
        :param angle: угол в градусах
        :return None:
        """
        if self.last_item is not None:
            pizza_ingredient, piece_index = self.last_item
            pizza_ingredient.position[piece_index][2] = angle
            self.update()

    def showEvent(self, event):
        """Установим фокус, чтобы сразу работали кнопки"""
        self.setFocus()
        super().showEvent(event)
