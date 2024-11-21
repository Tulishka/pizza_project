import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget, QApplication, QVBoxLayout, QStackedLayout, QSizePolicy
)

from screens.pizza_base import PizzaBaseWidget
from screens.pizza_editor import PizzaEditorWidget
from screens.welcome import WelcomeWidget


class PizzaConstructor(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Конструктор пиццы')
        self.setGeometry(300, 150, 1024, 728)
        self.setStyleSheet("background-color: white")
        self.setFixedSize(1024, 728)


        self.layout = QVBoxLayout(self)

        self.layout.setContentsMargins(0, 0, 0, 0)


        self.stack_layout = QStackedLayout(self)
        self.layout.addLayout(self.stack_layout)

        self.welcome_widget = WelcomeWidget(self)
        self.welcome_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.welcome_widget.next = self.pizza_base
        self.stack_layout.addWidget(self.welcome_widget)

        self.pizzabase_widget = PizzaBaseWidget(self)
        self.pizzabase_widget.next = self.pizza_edit
        self.pizzabase_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.stack_layout.addWidget(self.pizzabase_widget)

        self.pizzaedit_widget = PizzaEditorWidget(self)
        self.pizzaedit_widget.next = self.pizza_edit
        self.pizzaedit_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.stack_layout.addWidget(self.pizzaedit_widget)

        self.stack_layout.setCurrentWidget(self.welcome_widget)

    def pizza_base(self):
        self.stack_layout.setCurrentWidget(self.pizzabase_widget)

    def pizza_edit(self):
        self.stack_layout.setCurrentWidget(self.pizzaedit_widget)

        # self.setWindowState(Qt.WindowState.WindowFullScreen)
        # self.setWindowFlags(Qt.WindowType.FramelessWindowHint)


def func(*args):
    print(*args)
    sys.__excepthook__(*args)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    sys.excepthook = func
    ex = PizzaConstructor()
    ex.show()
    sys.exit(app.exec())
