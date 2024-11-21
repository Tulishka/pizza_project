from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout


class PaymentWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.setStyleSheet("""
            #label {
                font-size: 36pt;
            }
        """)

        self.next = None

        self.hlayout = QHBoxLayout(self)
        self.Vlayout = QVBoxLayout(self)
        self.hlayout.addLayout(self.vlayout)
        self.label = QLabel("Следуйте указаниям\nна терминале оплаты", self)
        self.vlayout.addWidget(self.label)
