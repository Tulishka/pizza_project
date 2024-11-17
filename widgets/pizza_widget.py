from PyQt6.QtGui import QPainter, QImage
from PyQt6.QtWidgets import QWidget, QSizePolicy


class PizzaWidget(QWidget):

    def __init__(self, parent):
        super().__init__(parent)
        self.setObjectName("pizzaWidget")
        # self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.pizza_base = QImage(f"images/ingredients/{'pizza_big_base'}.png")
        self.setMinimumSize(600, 600)
        self.pizza_base = self.pizza_base.scaled(self.width(), self.height())

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        cx, cy = self.width() // 2, self.height() // 2
        qp.drawImage(cx - self.pizza_base.width()//2, cy - self.pizza_base.height()//2, self.pizza_base)
        qp.end()
        super().paintEvent(event)
