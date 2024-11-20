from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSizePolicy, QHBoxLayout, QPushButton, QSpacerItem

import images_rep
from model import Ingredient, AddedIngredient


class AddedIngredientWidget(QWidget):
    removeRequest = pyqtSignal(object)

    def __init__(self, parent, ingredient: Ingredient, added_ingredient: AddedIngredient):
        super().__init__(parent)
        self.ingredient = ingredient
        self.added_ingredient = added_ingredient

        self.setStyleSheet("""
            #back {
                background-color: #DFDFDF;
                border-radius: 12px;
                padding: 12px;
            }
            
            QWidget {
                font-size: 16pt;
            }
            
            #icon {
                border-radius: 25px;
            }
            
            #remove_btn {
                color: #3D3D3D;
                background-color: #AFAFAF;
                padding: 12px 20px;
                border: 2px solid #00000000;
                border-radius: 15px;
            }
            
            #remove_btn:hover {
                background: #8F8F8F;
                border: 2px solid #666666
            }
            
        """)
        self.setObjectName("back")

        self.mlayout = QVBoxLayout(self)
        self.mlayout.setContentsMargins(0,0,0,0)
        self.widget = QWidget(self)
        self.widget.setMaximumWidth(parent.width()-10)
        self.widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)

        self.mlayout.addWidget(self.widget)

        self.hlayout = QHBoxLayout(self.widget)
        self.hlayout.setContentsMargins(0,0,0,0)
        self.hlayout.setSpacing(12)

        self.icon = QLabel(self.widget)
        self.icon.setObjectName("icon")
        self.icon.setPixmap(images_rep.get_pixmap(ingredient.get_icon_filename()).scaled(32, 32))
        self.icon.setFixedSize(32, 32)

        self.remove_btn = QPushButton("X", self.widget)
        self.remove_btn.setObjectName("remove_btn")
        self.remove_btn.clicked.connect(self.remove_cliecked)

        self.label = QLabel(ingredient.title, self.widget)
        self.label.setWordWrap(True)
        self.label.setMaximumWidth(150)

        self.hlayout.addWidget(self.icon)
        self.hlayout.addWidget(self.label)
        self.hlayout.addSpacerItem(QSpacerItem(1, 1, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        self.hlayout.addWidget(QLabel(f"{ingredient.get_portion_price(added_ingredient.portion_size)} ₽", self.widget))
        self.hlayout.addWidget(self.remove_btn)

        self.list_item = None

    def remove_cliecked(self):
        self.removeRequest.emit(self)
