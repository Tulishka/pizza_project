from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QVBoxLayout, QLabel, QHBoxLayout

from screens.BaseScreen import BaseScreen
from state import State


class CompleteWidget(BaseScreen):
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
        self.vlayout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignHCenter)

    def activated(self):
        self.label.setText(
            f"СПАСИБО ЗА ЗАКАЗ!\n"
            f"Наши повара уже трудятся\n"
            f"над вашим шедевром\n"
            f"Номер заказа: {State.order_number}"
        )
        super().activated()

    def prev_clicked(self):
        self.next.emit()
