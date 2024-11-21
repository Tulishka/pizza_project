from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton


class CompleteWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.setStyleSheet("""
            QPushButton {
                background-color: #EDEDED;
                border: 2px solid #C3C3C3;
                border-radius: 15px;
                padding: 10px;
                font-size: 16px;
            }        

            QLabel {
                font-size: 38pt;
            }
        """)

        self.next = None

        self.hlayout = QHBoxLayout(self)
        self.vlayout = QVBoxLayout(self)
        self.hlayout.addLayout(self.vlayout)
        self.label = QLabel(f"Спасибо за заказ!\nНаши повара уже трудятся\nнад вашим шедевром\nНомер заказа: {'0000'}", self)
        self.vlayout.addWidget(self.label)
        self.complete = QPushButton("Завершить", self)
        self.vlayout.addWidget(self.complete)
