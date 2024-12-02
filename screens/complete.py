from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QVBoxLayout, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy

import state
from screens.base import BaseScreen
from state import State


class CompleteWidget(BaseScreen):
    """Экран завершения заказа"""

    def __init__(self, parent):
        super().__init__(parent)

        self.setStyleSheet("""
            QLabel {
                font-size: 38pt;
            }
        """)

        self.hlayout = QHBoxLayout(self)
        self.vlayout = QVBoxLayout(self)
        self.hlayout.addLayout(self.vlayout)
        self.label = QLabel(self)
        self.img = QLabel(self)
        self.img.setStyleSheet("border-radius:15px")
        self.vlayout.addWidget(self.img, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.vlayout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.vlayout.addSpacerItem(QSpacerItem(1, 50, QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Minimum))

    def activated(self):
        """Обработчик экрана закрытия заказа: выводит картинку и номер заказа
        :return None:
        """

        self.img.setPixmap(
            state.State.pizza_image.scaled(
                state.State.pizza_image.width() // 2,
                state.State.pizza_image.height() // 2
            ))

        self.label.setText(
            f"СПАСИБО ЗА ЗАКАЗ!\n"
            f"Наши повара уже трудятся\n"
            f"над вашим шедевром\n"
            f"Номер заказа: {State.order.id}"
        )
        # Завершаем заказ
        state.order_complete()

    def prev_clicked(self):
        """Обработчик кнопки назад: поднимает сигнал next,
        так как экран последний, приведёт к переходу на начальный экран
        :return None:
        """

        self.next.emit()
