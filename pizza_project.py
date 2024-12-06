import sys

from PyQt6.QtWidgets import QApplication

from screens.terminal_main import PizzaConstructor

from screens.technolog_main import PizzaTechnolog


def exception_logger(*args):
    print(*args)
    sys.__excepthook__(*args)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    sys.excepthook = exception_logger

    if sys.argv[1:] and sys.argv[1:][0] == 'technolog':
        ex = PizzaTechnolog()
    else:
        ex = PizzaConstructor()

    ex.show()
    sys.exit(app.exec())
