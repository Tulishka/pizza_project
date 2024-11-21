import sys

from PyQt6.QtWidgets import (
    QWidget, QApplication, QVBoxLayout, QStackedLayout, QSizePolicy, QPushButton
)

import state  # создать состояние

import const
from screens import BaseScreen
from screens.complete import CompleteWidget
from screens.payment import PaymentWidget
from screens.pizza_base import PizzaBaseWidget
from screens.pizza_editor import PizzaEditorWidget
from screens.welcome import WelcomeWidget


class PizzaConstructor(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Конструктор пиццы')
        self.setGeometry(300, 150, const.MAIN_WINDOW_WIDTH, const.MAIN_WINDOW_HEIGHT)
        self.setStyleSheet("background-color: white")
        self.setFixedSize(const.MAIN_WINDOW_WIDTH, const.MAIN_WINDOW_HEIGHT)

        self.vlayout = QVBoxLayout(self)
        self.vlayout.setContentsMargins(0, 0, 0, 0)

        self.stack_layout = QStackedLayout(self)
        self.vlayout.addLayout(self.stack_layout)

        self.prev_button = QPushButton("< Назад", self)
        self.prev_button.move(12, 12)
        self.prev_button.setMinimumSize(130, 50)
        self.prev_button.hide()
        self.prev_button.clicked.connect(self.prev_clicked)

        self.screens_cls: list[BaseScreen] = [WelcomeWidget, PizzaBaseWidget, PizzaEditorWidget, PaymentWidget,
                                              CompleteWidget]
        self.screens = {}

        prev = None
        for screen_cls in self.screens_cls:
            screen_widget = screen_cls(self)
            screen_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            screen_widget.next.connect(self.next_screen)
            screen_widget.prev.connect(self.prev_screen)

            self.stack_layout.addWidget(screen_widget)
            self.screens[screen_cls] = [screen_widget, prev, None]
            prev = screen_widget

        for idx in range(len(self.screens_cls) - 1):
            self.screens[self.screens_cls[idx]][2] = self.screens[self.screens_cls[idx + 1]][0]

        self.stack_layout.setCurrentWidget(self.screens[self.screens_cls[0]][0])

    def activate_screen(self, screen: BaseScreen):
        self.stack_layout.setCurrentWidget(screen)
        screen.activated()

        if self.screens[type(screen)][1] is not None:
            screen.setup_prev_button(self.prev_button)
            self.prev_button.show()
            self.prev_button.raise_()
        else:
            self.prev_button.hide()

    def next_screen(self):
        screen_cls = type(self.sender())
        next_scr = self.screens[screen_cls][2]
        if not next_scr:
            next_scr = self.screens[self.screens_cls[0]][0]
        self.activate_screen(next_scr)

    def prev_screen(self):
        screen_cls = type(self.sender())
        prev_scr = self.screens[screen_cls][1]
        if prev_scr:
            self.activate_screen(prev_scr)

    def prev_clicked(self):
        self.stack_layout.currentWidget().prev_clicked()


def exception_logger(*args):
    print(*args)
    sys.__excepthook__(*args)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    sys.excepthook = exception_logger
    ex = PizzaConstructor()
    ex.show()
    sys.exit(app.exec())
