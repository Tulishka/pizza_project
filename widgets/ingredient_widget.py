from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSizePolicy

import images_rep
from model import Ingredient


class IngredientWidget(QWidget):
    def __init__(self, parent, ingredient: Ingredient):
        super().__init__(parent)
        self.resize(147, 174)
        self.setFixedSize(147, 174)
        self.setStyleSheet("""
            #back, QWidget {
                border-radius: 20px;
                background-color: #EFEFEF;
            }
            #back:hover {
                border: 2px solid #555555
            }
        """)
        self.mlayout = QVBoxLayout(self)
        self.widget = QWidget(self)
        self.widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.widget.setObjectName("back")
        self.mlayout.addWidget(self.widget)

        self.vlayout = QVBoxLayout(self.widget)
        self.icon = QLabel(self.widget)
        self.icon.setPixmap(images_rep.get_pixmap(ingredient.get_icon_filename()))
        self.icon.setFixedSize(64, 64)
        self.vlayout.addWidget(self.icon, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.vlayout.addWidget(QLabel(ingredient.title, self.widget), alignment=Qt.AlignmentFlag.AlignHCenter)
        self.vlayout.addWidget(QLabel(f"{ingredient.price} ₽", self.widget), alignment=Qt.AlignmentFlag.AlignHCenter)

        # self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
