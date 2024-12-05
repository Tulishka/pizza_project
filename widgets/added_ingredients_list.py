from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QListWidget, QListWidgetItem

from database import state
from database.model import AddedIngredient
from widgets.added_ingredient_widget import AddedIngredientWidget


class AddedIngredientsList(QListWidget):
    """Виджет списка добавленных ингредиентов"""

    itemRemoved = pyqtSignal(object)

    def __init__(self, parent):
        super().__init__(parent)
        self.setStyleSheet("background:#F0F0F0; border: none")
        self.setSpacing(8)

    def add_ingredient(self, added_ingredient: AddedIngredient):
        """Метод добавляет ингредиент в список
        :param added_ingredient:
        :return None:
        """
        ingredient_widget = AddedIngredientWidget(
            self,
            state.all_ingredients_dict[added_ingredient.ingredient_id],
            added_ingredient
        )

        ingredient_widget.removeRequest.connect(self.remove_item)

        item = QListWidgetItem()
        item.setSizeHint(ingredient_widget.sizeHint())
        ingredient_widget.list_item = item
        self.addItem(item)
        self.setItemWidget(item, ingredient_widget)

    def remove_item(self, item):
        """Метод удаляет ингредиент из списка
        :param item:
        :return None:
        """
        self.takeItem(self.row(item.list_item))
        self.itemRemoved.emit(item.added_ingredient)
