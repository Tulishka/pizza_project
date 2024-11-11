from PyQt6.QtWidgets import QListWidget


class OrderIngredientsList(QListWidget):
    def __init__(self, parent):
        super().__init__(parent)


    def add_ingredient(self, title, img_path, price, quantity):
        # Создаем экземпляр кастомного виджета
        ingredient_widget = IngredientWidget(title, img_path, price, quantity)
        # Создаем элемент списка и устанавливаем виджет
        item = QListWidgetItem()
        item.setSizeHint(ingredient_widget.sizeHint())  # Устанавливаем размер элемента списка
        self.list_widget.addItem(item)
        self.list_widget.setItemWidget(item, ingredient_widget)  # Устанавливаем кастомный виджет в элемент списка
