from PyQt6.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QLabel, QSizePolicy, QHBoxLayout, QListWidget
)

from model import current_pizza, AddedIngredient
from position_generators import pos_gen
from widgets.added_ingredients_list import AddedIngredientsList
from widgets.choice_ingredient import ChoiceIngredientDialog
from widgets.ingredient_options import IngredientOptionsDialog
from widgets.pizza_widget import PizzaWidget


class PizzaEditorWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.resize(self.parent().width(), self.parent().height())

        self.next = None

        self.back = QWidget(self)

        self.back.resize(self.parent().width(), self.parent().height())
        self.back.move(0, 0)
        self.back.setStyleSheet("""
            background-color: white;
            border-radius: 0;
            padding: 0;
            margin: 0;
        """)

        self.hlayout = QHBoxLayout(self)
        self.hlayout.setContentsMargins(0, 0, 0, 0)

        self.pizza_widget = PizzaWidget(self)
        self.hlayout.addWidget(self.pizza_widget)

        self.panel_widget = QWidget(self)
        # self.panel_widget.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        self.panel_widget.setStyleSheet("""
            background-color: #F0F0F0;
            border-radius: 0;
        """)
        self.hlayout.addWidget(self.panel_widget)
        self.panel_widget.setFixedWidth(390)

        self.vlayout = QVBoxLayout(self.panel_widget)
        self.vlayout.setSpacing(12)
        self.ingredients_label = QLabel("Ингредиенты:")
        self.ingredients_label.setStyleSheet("""
            font-size: 30pt
        """)
        self.vlayout.addWidget(self.ingredients_label)

        self.list_widget = AddedIngredientsList(self)
        self.list_widget.itemRemoved.connect(self.item_removed)
        self.vlayout.addWidget(self.list_widget)

        self.add_ing_layout = QHBoxLayout(self)
        self.vlayout.addLayout(self.add_ing_layout)
        self.add_button = QPushButton("+", self)
        self.add_button.clicked.connect(self.add_ingredient)
        self.remained_label = QLabel(f"ещё можно добавить\n{'00'} ингредиентов")
        self.remained_label.setStyleSheet("""
            font-size: 16pt
        """)
        self.add_button.setStyleSheet("""
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
        """)
        self.add_button.setMaximumWidth(100)
        self.add_button.setFixedHeight(60)

        self.add_ing_layout.addWidget(self.add_button)
        self.add_ing_layout.addWidget(self.remained_label)

        self.time_label = QLabel(f"Примерное время готовки: {'00:00'}", self)
        self.time_label.setStyleSheet("""
                    font-size: 18pt
                """)
        self.vlayout.addWidget(self.time_label)

        self.order_layout = QHBoxLayout(self)
        self.vlayout.addLayout(self.order_layout)
        self.res_sum_label = QLabel(f"К оплате:\n{'0000'} руб.")
        self.res_sum_label.setStyleSheet("""
                    font-size: 26pt
                """)
        self.order_layout.addWidget(self.res_sum_label)

        self.order_button = QPushButton("Заказать", self)
        self.order_button.setStyleSheet("""
            QPushButton {
                color: #black;
                background-color: #6CE08F;
                border: 2px solid #00000000;
                border-radius: 15px;
                padding: 10px;
                font-size: 30px;

            }        
            QPushButton:hover {
                border-color: #48A865;
            } 
        """)
        self.order_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        self.order_button.setFixedHeight(100)
        self.order_layout.addWidget(self.order_button)

        self.background = QWidget(self)
        self.background.setGeometry(0, 0, self.parent().width(), self.parent().height())
        self.background.setStyleSheet("""
                background-color: #DE000000;
        """)
        self.background.hide()

    # self.vlayout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

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
            positions = pos_gen.gen_ingredient_positions(current_pizza(), ing_dlg.ingredient, ing_count)

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
            self.pizza_widget.setup_components()
            self.update()

        finally:
            self.hide_background()

    def ok_click(self):
        self.next()


    def item_removed(self, remove_item: AddedIngredient):
        current_pizza().added_ingredients.remove(remove_item)
        self.pizza_widget.setup_components()
        self.update()
