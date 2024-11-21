from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout


class PaymentWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.setStyleSheet("""
            #back {
                background-color: white;
                border-radius: 0;
                padding: 0;
                margin: 0;
            }

            #ingredients_label {
                font-size: 36pt;
            }
        """)

        self.next = None

        self.vlayout = QVBoxLayout(self)
        self.hlayout = QHBoxLayout(self)
        self.vlayout.addLayout(self.hlayout)
        self.label = QLabel("Следуйте указаниям\nна терминале оплаты", self)
        self.hlayout.addWidget(self.label)
