from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QButtonGroup, \
    QSpacerItem

from utils import image_lib
from database.model import Ingredient
from widgets.pizza_button import PizzaButton


class IngredientOptionsDialog(QDialog):
    """Диалог выбора опций ингредиента (размера порции)"""

    def __init__(self, parent, ingredient: Ingredient):
        super().__init__(parent)

        self.ingredient = ingredient
        self.selected_size = 0

        self.setStyleSheet("""
                    #dialog {
                        border-radius: 15px;
                    }
        
                    QPushButton {
                        color: black;
                        background-color: #E4E4E4;
                        border: 2px solid #00000000;
                        border-radius: 15px;
                        padding: 10px;
                        font-size: 24px;

                    }        
                    QPushButton:hover {
                        border-color: #646464;
                    } 
                    
                    QPushButton#add:hover {
                        border-color: #39814E;
                    } 
                    
                    QPushButton:checked {
                        border: 2px solid #333333;
                        background-color: #D0D0D0;
                    }
                """)

        self.setObjectName("dialog")

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        self.setContentsMargins(0, 0, 0, 0)
        self.resize(671, 326)
        self.move(parent.width() // 2 - self.width() // 2, parent.height() // 2 - self.height() // 2)

        self.central_layout = QVBoxLayout(self)
        self.setLayout(self.central_layout)
        self.central_layout.setSpacing(40)

        self.label = QLabel("Выбери размер порции", self)
        self.label.setStyleSheet("""font-size: 32pt;""")

        self.cancel_btn = QPushButton("X", self)
        self.cancel_btn.setMaximumWidth(120)

        self.top_layout = QHBoxLayout(self)
        self.top_layout.addWidget(self.label)
        self.top_layout.addWidget(self.cancel_btn)

        self.img = QLabel(self)
        self.img.setFixedSize(120, 90)
        self.img.setPixmap(image_lib.get_pixmap(ingredient.get_image_filename()).scaled(90, 90))

        self.standard = PizzaButton(f"Стандартная\n{ingredient.get_portion_size(0)} шт.")
        self.standard.setFixedWidth(190)
        self.standard.setCheckable(True)
        self.standard.setChecked(True)

        self.big = PizzaButton(f"Большая\n{ingredient.get_portion_size(1)} шт.")
        self.big.setFixedWidth(190)
        self.big.setCheckable(True)

        self.size_layout = QHBoxLayout(self)
        self.size_layout.setSpacing(10)
        self.size_layout.setContentsMargins(50, 0, 10, 0)
        self.size_layout.addWidget(self.img)
        self.size_layout.addWidget(self.standard)
        self.size_layout.addWidget(self.big)
        self.size_layout.addSpacerItem(QSpacerItem(1, 1, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum))

        self.size_group = QButtonGroup(self)
        self.size_group.addButton(self.standard)
        self.size_group.addButton(self.big)

        self.price = QLabel(self)
        self.price.setStyleSheet("""font-size: 24pt;""")

        self.add = PizzaButton("Добавить", self)
        self.add.setStyleSheet("""font-size: 24pt;background: #6CE08F;""")
        self.add.setObjectName("add")

        self.add_layout = QHBoxLayout(self)
        self.add_layout.setSpacing(12)
        self.add_layout.addSpacerItem(QSpacerItem(1, 1, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum))
        self.add_layout.addWidget(self.price)
        self.add_layout.addWidget(self.add)

        self.central_layout.addLayout(self.top_layout)
        self.central_layout.addLayout(self.size_layout)
        self.central_layout.addLayout(self.add_layout)
        self.central_layout.addSpacerItem(QSpacerItem(1, 1, QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Minimum))

        self.size_group.buttonClicked.connect(self.size_clicked)
        self.add.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)

        self.size_clicked(self.standard)

    def size_clicked(self, button):
        """Обработчик нажатия кнопки размера порции
        :param button:
        :return None:
        """
        self.selected_size = 1 if button is self.big else 0
        self.price.setText(f"{self.ingredient.get_portion_price(self.selected_size)} ₽")
