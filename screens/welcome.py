from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QLabel, QSpacerItem,
    QSizePolicy
)

import const
from screens.BaseScreen import BaseScreen


class WelcomeWidget(BaseScreen):
    def __init__(self, parent):
        super().__init__(parent)

        self.setStyleSheet("""
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

        self.layout = QVBoxLayout(self)

        self.verticalSpacer = QSpacerItem(10, 50, QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        self.layout.addSpacerItem(self.verticalSpacer)

        self.img_label = QLabel(self)
        pixmap = QPixmap(const.APP_DIR + "images/welcome_image.png")
        self.img_label.setPixmap(pixmap)

        self.layout.addWidget(self.img_label)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.layout.addSpacerItem(self.verticalSpacer)

        self.start_button = QPushButton("Создать пиццу мечты", self)

        self.start_button.clicked.connect(self.start_click)

        self.layout.addWidget(self.start_button)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.layout.addSpacerItem(self.verticalSpacer)

        self.layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.resize(self.parent().width(), self.parent().height())

    def start_click(self):
        self.next.emit()
