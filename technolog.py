import csv
import sys
from functools import partial

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeySequence, QShortcut
from PyQt6.QtSql import QSqlTableModel, QSqlDatabase
from PyQt6.QtWidgets import (
    QWidget, QApplication, QVBoxLayout, QSizePolicy, QPushButton, QTableView, QTabWidget,
    QToolBar, QFileDialog, QMessageBox
)

import database.create_db as cr
from utils import const

cr.create_db()
cr.insert_data()


class NoEditIdModel(QSqlTableModel):
    def flags(self, index):
        if index.column() == 0:
            return Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled
        return super().flags(index)


class PizzaTechnolog(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Редактирование ингредиентов')
        self.setGeometry(300, 150, const.MAIN_WINDOW_WIDTH, const.MAIN_WINDOW_HEIGHT)
        self.setStyleSheet("background-color: white")

        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName("pizza_db.sqlite")

        models = [
            ('Ингредиенты', "ingredients"),
            ('Виды теста', "dough_types"),
            ('Соусы', "souses"),
            ('Категории ингредиентов', "categories"),
            ('Цены на основы', "base_prices"),
        ]

        self.vlayout = QVBoxLayout(self)
        self.vlayout.setContentsMargins(0, 0, 0, 0)

        self.toolbar = QToolBar(self)
        self.vlayout.addWidget(self.toolbar)

        buttons = [
            ("Добавить нов.", self.add_row, 'alt+n'),
            ("Удалить строки", self.delete_rows, 'alt+d'),
            ("Загрузить из CSV", self.load_from_cvs, 'alt+i'),
            ("Сохранить в CVS", self.save_to_cvs, 'alt+e'),
        ]

        for title, func, key in buttons:
            btn = QPushButton(f"{title} [{key}]", self)
            btn.clicked.connect(func)
            btn.setShortcut(key)
            self.toolbar.addWidget(btn)

        self.tab_widget = QTabWidget(self)
        self.tab_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)


        for idx, (title, table_name) in enumerate(models):
            shortcut = QShortcut(QKeySequence("Ctrl+" + str(idx + 1)), self)
            shortcut.tab_index = idx
            shortcut.activated.connect(partial(self.shortcut_table, idx))

            model = NoEditIdModel()
            model.setTable(table_name)
            model.select()

            tab = QTableView(self)
            tab.resize(self.width(), self.height())
            tab.setModel(model)
            tab.setEditTriggers(
                QTableView.EditTrigger.DoubleClicked | QTableView.EditTrigger.EditKeyPressed
            )
            tab.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            self.tab_widget.addTab(tab, title + f" [Ctrl+{idx + 1}]")

        self.vlayout.addWidget(self.tab_widget)

    def current_model(self) -> QSqlTableModel:
        return self.tab_widget.currentWidget().model()

    def current_view(self) -> QTableView:
        return self.tab_widget.currentWidget()

    def add_row(self):
        self.current_model().insertRow(self.current_model().rowCount())

    def delete_rows(self):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Подтвердите")
        msg_box.setText("Удалить выбранные строки (может привести к не правильной работе программы)?")
        msg_box.setIcon(QMessageBox.Icon.Question)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
        result = msg_box.exec()
        if result == QMessageBox.StandardButton.Cancel:
            return

        model = self.current_model()
        selected_indexes = self.current_view().selectedIndexes()
        for index in selected_indexes:
            model.removeRow(index.row())
        model.submitAll()
        model.select()

    def load_from_cvs(self):
        model = self.current_model()
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Загрузить из CSV", model.tableName(), "CSV файлы (*.csv);;Все файлы (*)"
        )
        if file_name:
            with open(file_name, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)
                model.removeRows(0, model.rowCount())
                for row in reader:
                    model.insertRow(model.rowCount())
                    for column, value in enumerate(row):
                        if column != 0:
                            model.setData(model.index(model.rowCount() - 1, column), value)
                    model.submitAll()

            model.select()

    def save_to_cvs(self):
        model = self.current_model()
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Сохранить в CSV", model.tableName(), "CSV Files (*.csv);;All Files (*)"
        )
        if file_name:
            with open(file_name, mode='w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                headers = [model.headerData(i, Qt.Orientation.Horizontal) for i in range(model.columnCount())]
                writer.writerow(headers)
                for row in range(model.rowCount()):
                    row_data = []
                    for column in range(model.columnCount()):
                        row_data.append(model.data(model.index(row, column)))
                    writer.writerow(row_data)

    def shortcut_table(self, idx: int):
        self.tab_widget.setCurrentIndex(idx)


def exception_logger(*args):
    print(*args)
    sys.__excepthook__(*args)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    sys.excepthook = exception_logger
    ex = PizzaTechnolog()
    ex.show()
    sys.exit(app.exec())
