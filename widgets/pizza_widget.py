from PyQt6.QtWidgets import QWidget, QSizePolicy


class PizzaWidget(QWidget):

    def __init__(self, parent):
        super().__init__(parent)

        self.setObjectName("pizzaWidget")
        # self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.setMinimumSize(600, 600)
