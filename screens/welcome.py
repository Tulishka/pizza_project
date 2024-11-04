from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QLabel, QSpacerItem,
    QSizePolicy
)

class WelcomeWidget(QWidget):
    def __init__(self, *args):
        super().__init__(*args)

        self.layout = QVBoxLayout(self)

        self.verticalSpacer = QSpacerItem(10, 50, QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        self.layout.addSpacerItem(self.verticalSpacer)

        self.img_label = QLabel(self)
        pixmap = QPixmap("./images/welcome_image.png")
        self.img_label.setPixmap(pixmap)
        self.layout.addWidget(self.img_label)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.layout.addSpacerItem(self.verticalSpacer)


        self.start_button = QPushButton("Создать пиццу мечты", self)
        self.start_button.setStyleSheet("""
        QPushButton {
            background-color: #6CE08F;
            border: 2px solid darkgreen;
            border-radius: 15px;
            padding: 10px;
            font-size: 32px;
        }        
        QPushButton:hover {
            background-color: darkgreen;
            color: white;
        }        
        """)

        self.layout.addWidget(self.start_button)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.layout.addSpacerItem(self.verticalSpacer)

        self.layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.resize(1024, 728)
