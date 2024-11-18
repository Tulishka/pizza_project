from PyQt6.QtGui import QPainter, QImage
from PyQt6.QtWidgets import QWidget, QSizePolicy

from model import Ingredient


class PizzaWidget(QWidget):

    def __init__(self, parent):
        super().__init__(parent)
        self.setObjectName("pizzaWidget")
        # self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.setMinimumSize(600, 600)

        self.pizza_base = QImage(f"images/ingredients/{'pizza_big_base'}.png")
        self.pizza_base = self.pizza_base.scaled(self.width(), self.height())

        self.sauce_img = QImage(f"images/ingredients/{'tomato_sauce'}.png")
        self.sauce_img = self.sauce_img.scaled(self.width(), self.height())

        # self.images = [Ingredient('mozzarella',), 'olive', 'pepperoni']

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        cx, cy = self.width() // 2, self.height() // 2
        qp.drawImage(cx - self.pizza_base.width()//2, cy - self.pizza_base.height()//2, self.pizza_base)
        qp.drawImage(cx - self.pizza_base.width()//2, cy - self.pizza_base.height()//2, self.sauce_img)
        # for i in self.images:
        #     img = QImage(f"images/ingredients/{'tomato_sauce'}.png")
        #     img = img.scaled(self.width(), self.height())
        #     qp.drawImage(20, 40, img)

        qp.end()
        super().paintEvent(event)
