from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout

import state


class PaymentWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.setStyleSheet("""
            QLabel {
                font-size: 30pt;
            }
        """)

        self.next = None

        self.vlayout = QVBoxLayout(self)
        self.price = QLabel(f"Оплатите {state.current_pizza_total_cost()} ₽", self)
        self.label = QLabel("Следуйте указаниям\nна терминале оплаты", self)
        self.vlayout.addWidget(self.price, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.vlayout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignHCenter)
