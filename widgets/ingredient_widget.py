from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QMouseEvent
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSizePolicy

from utils import image_lib
from model import Ingredient


class IngredientWidget(QWidget):
    """Виджет для отображения ингредиента в диалоге добавления"""

    clicked = pyqtSignal(object, name="clicked")

    def __init__(self, parent, ingredient: Ingredient):
        super().__init__(parent)
        self.ingredient = ingredient

        self.setStyleSheet("""
            #back, QWidget {
                border-radius: 15px;
                background-color: #EFEFEF;
            }
            #back:hover {
                border: 2px solid #555555
            }
            QLabel {
                font-size: 13px;
            }
        """)

        self.setMaximumWidth(147)
        self.setMaximumHeight(174)
        self.setMinimumHeight(140)

        self.mlayout = QVBoxLayout(self)
        self.widget = QWidget(self)
        self.widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.widget.setObjectName("back")
        self.mlayout.addWidget(self.widget)

        self.vlayout = QVBoxLayout(self.widget)
        self.icon = QLabel(self.widget)
        self.icon.setPixmap(image_lib.get_pixmap(ingredient.get_icon_filename()))
        self.icon.setFixedSize(64, 64)
        self.vlayout.addWidget(self.icon, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.vlayout.addWidget(QLabel(ingredient.title, self.widget), alignment=Qt.AlignmentFlag.AlignHCenter)
        self.vlayout.addWidget(QLabel(f"{ingredient.price} ₽", self.widget), alignment=Qt.AlignmentFlag.AlignHCenter)

    def mousePressEvent(self, event: QMouseEvent):
        """Обработчик нажатия на виджет, отправляет сигнал clicked
        :param event:
        :return None:
        """
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.ingredient)
