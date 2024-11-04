import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QWidget, QApplication, QPushButton, QVBoxLayout, QStackedLayout, QLabel, QSpacerItem,
    QSizePolicy
)

from screens.welcome import WelcomeWidget


class PizzaConstructor(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Конструктор пиццы')

        self.layout = QVBoxLayout(self)
        self.stack_layout = QStackedLayout(self)

        self.welcome_widget = WelcomeWidget(self)
        self.stack_layout.setCurrentWidget(self.welcome_widget)

        self.layout.addLayout(self.stack_layout)

        self.setGeometry(300, 150, 1024, 728)
        self.setStyleSheet("background-color: white;")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PizzaConstructor()
    ex.show()
    sys.exit(app.exec())
