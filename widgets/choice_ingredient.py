from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QButtonGroup, \
    QGridLayout, QStackedLayout, QWidget

import db
import model
from db import get_model
from model import Ingredient
from widgets.ingredient_widget import IngredientWidget


class ChoiceIngredientDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        self.setContentsMargins(0, 0, 0, 0)
        self.resize(720, 490)
        self.move(parent.width() // 2 - self.width() // 2, parent.height() // 2 - self.height() // 2)

        self.central_layout = QVBoxLayout(self)
        self.setLayout(self.central_layout)
        self.central_layout.setSpacing(8)

        self.top_layout = QHBoxLayout(self)
        self.central_layout.addLayout(self.top_layout)

        self.label = QLabel("Выбери ингредиент", self)

        self.label.setStyleSheet("""
                font-size: 32pt;
        """)

        self.cancel_btn = QPushButton("X", self)
        self.cancel_btn.setStyleSheet("""
            QPushButton {
                color: #black;
                background-color: #E4E4E4;
                border: 2px solid #00000000;
                border-radius: 15px;
                padding: 10px;
                font-size: 24px;

            }        
            QPushButton:hover {
                border-color: #646464;
            } 
        """)
        self.cancel_btn.setMaximumWidth(120)
        self.cancel_btn.clicked.connect(self.cancel_click)

        self.top_layout.addWidget(self.label)
        self.top_layout.addWidget(self.cancel_btn)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        self.setStyleSheet("""
            #dialog{
                border-radius: 15px;
            }
                
            QPushButton {
                background-color: #EFE4D8;
                border: 2px solid #00000000;
                border-radius: 15px;
                padding: 10px;
                font-size: 16px;
            }        
            QPushButton:hover {
                border-color: #555555;
            } 
            
            QPushButton#category {
                font-size: 32px;
                background-color: #EFE4D8;
            } 
            
            QPushButton#category:checked {
                border: 2px solid #333333;
                background-color: #D6C7B6;
            }
                
        """)

        all_ingredients = db.get_model_cached(Ingredient)

        self.setObjectName("dialog")
        self.ingredient = None

        self.category_layout = QHBoxLayout(self)
        self.central_layout.addLayout(self.category_layout)
        self.categories = QButtonGroup(self)

        self.stack_layout = QStackedLayout(self)
        self.central_layout.addLayout(self.stack_layout)

        for idx, category in enumerate(db.get_model_cached(model.IngredientCategory)):
            button = QPushButton(category.title, self)
            button.setObjectName("category")
            button.index = idx

            self.categories.addButton(button)
            self.category_layout.addWidget(button)
            button.setCheckable(True)
            button.setChecked(idx == 0)

            grid_widget = QWidget(self)
            grid_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            grid_layout = QGridLayout(grid_widget)
            grid_layout.setSpacing(8)

            self.stack_layout.addWidget(grid_widget)
            for i, ing in enumerate(ind for ind in all_ingredients if ind.category_id == category.id):
                iw = IngredientWidget(self, ing)
                iw.clicked.connect(self.ingredient_selected)
                grid_layout.addWidget(iw, i // 4, i % 4)

        self.stack_layout.setCurrentIndex(0)
        self.categories.buttonClicked.connect(self.category_clicked)

    def category_clicked(self, button):
        self.stack_layout.setCurrentIndex(button.index)

    def cancel_click(self):
        self.reject()

    def ingredient_selected(self, ingredient: Ingredient):
        self.ingredient=ingredient
        self.accept()
