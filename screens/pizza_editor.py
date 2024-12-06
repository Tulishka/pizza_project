from random import randint

from PyQt6.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QLabel, QSizePolicy, QHBoxLayout, QMessageBox, QListWidget
)

from utils import const
from database import state
from database.model import AddedIngredient
from screens.base import BaseScreen
from database.state import current_pizza
from utils.position_generators import pos_gen
from widgets.added_ingredients_list import AddedIngredientsList
from widgets.choice_ingredient import ChoiceIngredientDialog
from widgets.ingredient_options import IngredientOptionsDialog
from widgets.pizza_widget import PizzaWidget


class PizzaEditorWidget(BaseScreen):
    """Экран редактора пиццы"""

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
        self.list_widget.itemsOrdered.connect(self.items_ordered)
        self.list_widget.setDragDropMode(QListWidget.DragDropMode.InternalMove)
        self.list_widget.setAcceptDrops(True)

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
        self.order_button.clicked.connect(self.order_click)

        self.background = QWidget(self)
        self.background.setGeometry(0, 0, self.parent().width(), self.parent().height())
        self.background.setObjectName("background")
        self.background.hide()

        self.total_sum = 0
        self.prev_button = None

    def setup_prev_button(self, btn):
        """Обработчик для настройки кнопки назад, сохраняем кнопку, чтобы потом скрывать её
        :param btn:
        :return None:
        """
        super().setup_prev_button(btn)
        self.prev_button = btn

    def activated(self):
        """Обработчик открытия экрана редактора пиццы
        :return None:
        """
        if not current_pizza().added_ingredients:
            self.list_widget.clear()
        self.pizza_widget.setup_pizza_base()
        self.pizza_updated()

    def show_background(self):
        """Метод показывает затемнённый фон и скрывает кнопку назад
        :return None:
        """
        self.background.show()
        self.prev_button.hide()

    def hide_background(self):
        """Метод убирает затемнённый фон и делает видимой кнопку назад
        :return None:
        """
        self.background.hide()
        self.prev_button.show()

    def add_ingredient(self):
        """Метод добавляет новый ингредиент в пиццу
        :return None:
        """
        self.show_background()
        try:
            # Открытие диалога для выбора ингредиента
            ing_dlg = ChoiceIngredientDialog(self)
            if ing_dlg.exec() == 0:
                return

            # Открытие диалога для выбора опций (размер порции)
            opt_dlg = IngredientOptionsDialog(self, ing_dlg.ingredient)
            if opt_dlg.exec() == 0:
                return

            # Получим количество кусочков ингредиента для добавления
            ing_count = ing_dlg.ingredient.get_portion_size(opt_dlg.selected_size)

            # Генерируем начальные позиции для всех новых кусочков
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
            # Добавим новый ингредиент в список добавленных ингредиентов
            self.list_widget.add_ingredient(item)
            self.pizza_updated()


        finally:
            self.hide_background()

    def order_click(self):
        """Обработчик для кнопки заказать
        :return None:
        """
        # Создание объекта заказа
        state.save_order(current_pizza(), state.current_pizza_total_cost())

        # Сохранение изображения пиццы в файл и в state
        self.pizza_widget.angleSlider.hide()
        capturedImage = self.pizza_widget.grab()
        filename = f"{const.PIZZAS_PICTURES_DIR}/pizza_order_{state.State.order.id}_{randint(1000, 9999)}.png"
        capturedImage.save(filename)
        state.set_pizza_picture(filename, capturedImage)

        # переход на следующий экран
        self.next.emit()

    def pizza_updated(self):
        """Метод должен быть вызван после изменения объекта пиццы.
        Обновляет элементы на экране
        :return None:
        """
        total_sum = state.current_pizza_total_cost()
        self.res_sum_label.setText(f"К оплате:\n{total_sum} ₽")
        self.pizza_widget.setup_components()
        remain = const.PIZZA_MAX_INGREDIENTS[current_pizza().size] - state.current_pizza_ingredients_count()
        if remain > 0:
            self.remained_label.setText(f"ещё можно добавить\n{remain} ингредиентов")
        else:
            self.remained_label.setText(f"Вы добавили максимум\nингредиентов!")
        self.add_button.setEnabled(remain > 0)
        self.update()

    def item_removed(self, remove_item: AddedIngredient):
        """Обработчик удаления ингредиента, вызывается при удалении элемента
        :return None:
        """
        current_pizza().added_ingredients.remove(remove_item)
        self.pizza_updated()

    def prev_clicked(self):
        """Обработчик нажатия кнопки назад, спрашивает подтверждение отмены пиццы
        :return None:
        """
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Подтвердите")
        msg_box.setText("Отменить создание пиццы?")
        msg_box.setIcon(QMessageBox.Icon.Question)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
        result = msg_box.exec()
        if result == QMessageBox.StandardButton.Cancel:
            return
        super().prev_clicked()

    def items_ordered(self):
        """Обработчик события - изменения порядка ингредиентов"""
        new_order = []
        for i in range(self.list_widget.count()):
            new_order.append(self.list_widget.itemWidget(self.list_widget.item(i)).added_ingredient)

        current_pizza().added_ingredients = new_order

        self.pizza_widget.setup_components()
        self.update()
