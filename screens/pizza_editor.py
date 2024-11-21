from PyQt6.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QLabel, QSizePolicy, QHBoxLayout
)

import db
from db import get_model_cached
from model import AddedIngredient, Ingredient
from state import current_pizza
from utils.position_generators import pos_gen
from widgets.added_ingredients_list import AddedIngredientsList
from widgets.choice_ingredient import ChoiceIngredientDialog
from widgets.ingredient_options import IngredientOptionsDialog
from widgets.pizza_widget import PizzaWidget


class PizzaEditorWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.resize(self.parent().width(), self.parent().height())

        self.setStyleSheet("""
            #back {
                background-color: white;
                border-radius: 0;
                padding: 0;
                margin: 0;
            }
            
            #ingredients_label {
                font-size: 30pt;
            }
            
            #remained_label {
                font-size: 16pt;
            }
            
            #res_sum_label {
                font-size: 26pt;
            }
            
            QPushButton {
                color: #3D3D3D;
                background-color: #AFAFAF;
                border: 2px solid #00000000;
                border-radius: 15px;
                padding: 2px;
                font-size: 25px;
                
            }        
            
            QPushButton:hover {
                border-color: #555555;
            }
            
            QPushButton#order_button {
                color: black;
                background-color: #6CE08F;
                padding: 10px;
                font-size: 30px;

            }        
            
            QPushButton#order_button:hover {
                border-color: #48A865;
            } 
             
            #background {
                background-color: #DE000000;
            }

            #panel_widget, #panel_widget > QLabel {
                background-color: #F0F0F0;
                border-radius: 0;
            }
            
            
        """)

        self.next = None

        self.back = QWidget(self)

        self.back.resize(self.parent().width(), self.parent().height())
        self.back.move(0, 0)
        self.back.setObjectName('back')

        self.hlayout = QHBoxLayout(self)
        self.hlayout.setContentsMargins(0, 0, 0, 0)

        self.pizza_widget = PizzaWidget(self)
        self.hlayout.addWidget(self.pizza_widget)

        self.panel_widget = QWidget(self)
        self.panel_widget.setObjectName('panel_widget')
        self.panel_widget.setFixedWidth(390)

        self.hlayout.addWidget(self.panel_widget)

        self.vlayout = QVBoxLayout(self.panel_widget)
        self.vlayout.setSpacing(12)
        self.ingredients_label = QLabel("Ингредиенты:")
        self.ingredients_label.setObjectName('ingredients_label')

        self.vlayout.addWidget(self.ingredients_label)

        self.list_widget = AddedIngredientsList(self)
        self.list_widget.itemRemoved.connect(self.item_removed)
        self.vlayout.addWidget(self.list_widget)

        self.add_ing_layout = QHBoxLayout(self)
        self.vlayout.addLayout(self.add_ing_layout)
        self.add_button = QPushButton("+", self)
        self.add_button.clicked.connect(self.add_ingredient)
        self.remained_label = QLabel(f"ещё можно добавить\n{'00'} ингредиентов")
        self.remained_label.setObjectName('remained_label')
        self.add_button.setObjectName("add_button")

        self.add_button.setMaximumWidth(100)
        self.add_button.setFixedHeight(60)

        self.add_ing_layout.addWidget(self.add_button)
        self.add_ing_layout.addWidget(self.remained_label)

        self.order_layout = QHBoxLayout(self)
        self.vlayout.addLayout(self.order_layout)
        self.res_sum_label = QLabel(self)
        self.res_sum_label.setObjectName("res_sum_label")
        self.order_layout.addWidget(self.res_sum_label)

        self.order_button = QPushButton("Заказать", self)
        self.order_button.setObjectName("order_button")
        self.order_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        self.order_button.setFixedHeight(100)
        self.order_layout.addWidget(self.order_button)

        self.background = QWidget(self)
        self.background.setGeometry(0, 0, self.parent().width(), self.parent().height())
        self.background.setObjectName("background")
        self.background.hide()

        self.all_ingredients_dict = get_model_cached(Ingredient)

    def show_background(self):
        self.background.show()

    def hide_background(self):
        self.background.hide()

    def add_ingredient(self):
        self.show_background()
        try:
            ing_dlg = ChoiceIngredientDialog(self)
            if ing_dlg.exec() == 0:
                return

            opt_dlg = IngredientOptionsDialog(self, ing_dlg.ingredient)
            if opt_dlg.exec() == 0:
                return

            ing_count = ing_dlg.ingredient.get_portion_size(opt_dlg.selected_size)
            positions = pos_gen.generate_positions(current_pizza(), ing_dlg.ingredient, ing_count)

            item = AddedIngredient(
                0, 0,
                ingredient_id=ing_dlg.ingredient.id,
                addition_order=len(current_pizza().added_ingredients),
                count=ing_count,
                portion_size=opt_dlg.selected_size,
                position=positions
            )
            current_pizza().added_ingredients.append(item)
            self.list_widget.add_ingredient(item)
            self.pizza_updated()


        finally:
            self.hide_background()

    def ok_click(self):
        self.next()

    def pizza_updated(self):
        total_sum = db.get_base_price(current_pizza())
        for ingredient in current_pizza().added_ingredients:
            total_sum += self.all_ingredients_dict[ingredient.ingredient_id].get_portion_price(ingredient.portion_size)
        self.res_sum_label.setText(f"К оплате:\n{total_sum} ₽")
        self.pizza_widget.setup_components()
        self.update()

    def item_removed(self, remove_item: AddedIngredient):
        current_pizza().added_ingredients.remove(remove_item)
        self.pizza_updated()
